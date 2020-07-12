import pymzml
import ROIdetection
import numpy as np


def main():
    rois = []
    dead_rois = []
    threshold = 50000
    run = pymzml.run.Reader(
        "/Users/salvatoreesposito/Downloads/Beer_multibeers_1_fullscan1.mzML")
    for scan in list(run)[0:5]:
        # for scan in run:
        # mz can go into any ROI, but not mulitple roi
        extended_rois = []
        for idx, mz in enumerate(scan.mz):
            if scan.i[idx] < threshold:
                continue
            else:
                if rois == []:
                    peak = ROIdetection.Peak(
                        mz, scan.scan_time[0], scan.i[idx], scan)
                    roi = ROIdetection.ROI(peak)
                    extended_rois.append(roi)
                # here we create a new ROI
                else:
                    rois_mzs = [roi.mean_mz for roi in rois]
                    dist = abs(rois_mzs - mz)
                    closest_dist = np.array(dist).min()
                    if closest_dist < threshold:
                        closest_roi_index = np.argmin(np.array(dist))
                        peak = ROIdetection.Peak(
                            mz, scan.scan_time[0], scan.i[idx], scan)
                        rois[closest_roi_index].peak_list.append(peak)
                        extended_rois.append(rois[closest_roi_index])
                        rois.remove(rois[closest_roi_index])
                    # here we can add to an existing ROI
                    else:
                        peak = ROIdetection.Peak(
                            mz, scan.scan_time[0], scan.i[idx], scan)
                        roi = ROIdetection.ROI(peak)
                        extended_rois.append(roi)
                dead_rois = dead_rois + rois
                rois = extended_rois

    dead_rois = dead_rois + extended_rois
    print(extended_rois)

    completed_rois = []
    for saved_roi in dead_rois:
        peaklist = saved_roi.peak_list
        pmin = np.array([peak.mz for peak in peaklist]).min()
        if pmin < threshold:
            completed_rois.append(saved_roi)

    for roi in completed_rois:
        print("ROI")
        for peak in roi.peak_list:
            print(peak)


# if __name__ == "__main__":
main()
