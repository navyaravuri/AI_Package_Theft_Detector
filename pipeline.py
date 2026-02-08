from openfilter.filter_runtime.filters.video_in import VideoIn
from openfilter.filter_runtime.filters.webvis import Webvis
from openfilter_package_filter import PackageTheftFilter, PackageTheftFilterConfig
from openfilter.filter_runtime import Filter

if __name__ == "__main__":
    Filter.run_multi([
        # Step 1: Video input
        (VideoIn, dict(sources='file://your_video.mp4', outputs='tcp://*')),
        
        # Step 2: Custom package theft filter
        (PackageTheftFilter, dict(config=PackageTheftFilterConfig())),
        
        # Step 3: Web interface to view results
        (Webvis, dict(sources='tcp://localhost'))
    ])
