"""
Feature Extractor

Extracts OpenCV features useful for
Screenshot vs Wallpaper classification.
"""

import cv2
import numpy as np


class FeatureExtractor:

    # All the pixel-area thresholds below (icon size, widget size, text
    # box size, grid clustering tolerance) were effectively calibrated
    # for typical phone/tablet screenshot resolutions (~1080-1440px
    # wide). Camera photos in the same dataset are often 3000-4500px+
    # wide, where fine natural texture (leaves, gravel, grain) produces
    # thousands of small blobs that coincidentally fall in the same
    # *absolute* pixel-area range as real UI icons, purely because the
    # image is physically larger. Normalizing every image to a standard
    # width first makes every downstream area/size threshold apples-to
    # -apples regardless of the original resolution.
    REFERENCE_WIDTH = 1080

    def extract(self, image):

        orig_h, orig_w = image.shape[:2]

        if orig_w != self.REFERENCE_WIDTH:
            scale = self.REFERENCE_WIDTH / orig_w
            image = cv2.resize(
                image,
                (self.REFERENCE_WIDTH, int(round(orig_h * scale))),
                interpolation=cv2.INTER_AREA,
            )

        h, w = image.shape[:2]

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # -----------------------------------------
        # Edge Density
        # -----------------------------------------

        edges = cv2.Canny(gray, 80, 160)

        edge_density = np.count_nonzero(edges) / (h * w)

        # -----------------------------------------
        # Text Density / Text Regions
        # -----------------------------------------
        # text_boxes: any small horizontally-elongated blob (general text).
        # text_regions: the subset of those that look like short app/icon
        # labels (low height, tighter aspect ratio) — used by the
        # screenshot detector as a "home screen labels" signal.

        grad = cv2.Sobel(gray, cv2.CV_32F, 1, 0)

        grad = cv2.convertScaleAbs(grad)

        _, binary = cv2.threshold(
            grad,
            45,
            255,
            cv2.THRESH_BINARY,
        )

        contours, _ = cv2.findContours(
            binary,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        text_boxes = 0
        text_regions = 0

        for c in contours:

            x, y, ww, hh = cv2.boundingRect(c)

            area = ww * hh

            if 20 < area < 3000:

                ratio = ww / max(hh, 1)

                if 1 < ratio < 20:

                    text_boxes += 1

                    # Icon/app labels are short, squat strips of text
                    # sitting directly under an icon glyph.
                    if hh < 25 and 1.2 < ratio < 8:
                        text_regions += 1

        # -----------------------------------------
        # Top Status Bar
        # -----------------------------------------

        top = gray[: int(h * 0.08), :]

        top_edges = cv2.Canny(top, 50, 150)

        top_density = np.count_nonzero(top_edges) / top_edges.size

        # -----------------------------------------
        # Bottom Navigation Bar
        # -----------------------------------------

        bottom = gray[int(h * 0.90):, :]

        bottom_edges = cv2.Canny(bottom, 50, 150)

        bottom_density = np.count_nonzero(bottom_edges) / bottom_edges.size

        # -----------------------------------------
        # Icon Count / Widget Count / Grid Score
        # -----------------------------------------
        # Icons: small, roughly square blobs (app glyphs).
        # Widgets: larger, wider rectangular blobs (clock/weather/etc).
        # Grid score: how strongly icon centers line up on shared
        # rows/columns, which is characteristic of a home-screen grid.

        # Light blur before thresholding kills fine JPEG/WEBP-block and
        # texture noise (foliage, gravel, fabric, skin) so it never turns
        # into a spurious contour in the first place. Real icon/widget
        # tiles are flat and crisp enough to survive a 3x3 blur intact.
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        thresh = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY_INV,
            21,
            10,
        )

        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        icon_count = 0
        widget_count = 0
        icon_boxes = []

        for c in contours:

            x, y, ww, hh = cv2.boundingRect(c)

            area = ww * hh

            ratio = ww / max(hh, 1)

            # Solidity = contour area / convex-hull area. Icons and
            # widget tiles are clean, filled rounded-rectangles, so
            # solidity sits close to 1.0. Texture noise from photos
            # (leaves, gravel, clouds) produces jagged, concave blobs
            # with noticeably lower solidity — this is the main filter
            # that keeps busy wallpapers from being counted as "icons".
            hull = cv2.convexHull(c)
            hull_area = cv2.contourArea(hull)
            solidity = (cv2.contourArea(c) / hull_area) if hull_area > 0 else 0

            if solidity < 0.85:
                continue

            if 400 < area < 9000:

                if 0.75 < ratio < 1.3:

                    icon_count += 1

                    icon_boxes.append((x, y, ww, hh))

            elif 9000 <= area < 40000:

                # Widgets are noticeably wider than tall (clock,
                # weather, media strips), unlike a square icon glyph.
                if 1.3 <= ratio < 4.0:

                    widget_count += 1

        grid_score = self._grid_score(icon_boxes, w, h)

        return {

            "width": w,

            "height": h,

            "edge_density": edge_density,

            "text_boxes": text_boxes,

            "text_regions": text_regions,

            "top_density": top_density,

            "bottom_density": bottom_density,

            "icon_count": icon_count,

            "widget_count": widget_count,

            "grid_score": grid_score,

        }

    def _grid_score(self, boxes, w, h):

        # Need at least a few icons before "grid alignment" means anything.
        if len(boxes) < 3:
            return 0.0

        centers_x = [x + ww / 2 for x, y, ww, hh in boxes]
        centers_y = [y + hh / 2 for x, y, ww, hh in boxes]

        tol_x = w * 0.03
        tol_y = h * 0.03

        def cluster(values, tol):

            values = sorted(values)

            clusters = []

            for v in values:

                placed = False

                for cl in clusters:

                    if abs(cl[0] - v) < tol:
                        cl.append(v)
                        placed = True
                        break

                if not placed:
                    clusters.append([v])

            return clusters

        col_clusters = cluster(centers_x, tol_x)
        row_clusters = cluster(centers_y, tol_y)

        # An icon "counts" as grid-aligned if it shares a column or row
        # with at least one other icon.
        aligned = 0

        for cl in col_clusters:
            if len(cl) >= 2:
                aligned += len(cl)

        for cl in row_clusters:
            if len(cl) >= 2:
                aligned += len(cl)

        total_possible = len(boxes) * 2

        return round(min(aligned / total_possible, 1.0), 3)


feature_extractor = FeatureExtractor()