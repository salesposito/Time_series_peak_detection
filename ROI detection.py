import pymzml


class Peak(object):
    def __init__(self, mz, rt, intensity, scan_no):
        self.mz = mz
        self.rt = rt
        self.intensity = intensity
        self.scan_no = scan_no

    def __str__(self):
        return "({}, {})".format(self.mz, self.rt)


class ROI(object):
    def __init__(self, peak):
        self.peak_list = []
        self.peak_list.append(peak)
        self.update_mean_mz()

    def update_mean_mz(self):
        total = 0
        for peak in self.peak_list:
            total += peak.mz
            self.mean_mz = total / len(self.peak_list)

    def add_peak_to_roi(self, peak):
        self.peak_list.append(peak)
        self.update_mean_mz()

    def get_start_rt(self):
        return self.peak_list[0].rt  # assumes peaks are always in rt order

    def get_end_rt(self):
        return self.peak_list[-1].rt

    def processScans(self, path):
        run = pymzml.run.Reader(path)
        firstScan = run[0]
        firstScanRois = self.get_ROIs(firstScan)
        rois = []
        for scan in run[1:]:
            newRois = self.get_ROIs(scan)
            for roi in newRois:
                for firstroi in firstScanRois:
                    rois.append(roi)

        return rois

    def get_ROIs(self, scan):
        # read all scans in mzML file
        rois = []
        for peak in scan:
            p = peak(peak.mz, peak.rt, peak.intensity)
            roi = ROI(p)
            rois.append(roi)
        return rois