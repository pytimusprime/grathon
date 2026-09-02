"""
Auto-Download Manager
Configure and monitor auto-download settings in TDLib
"""

from typing import Optional, Callable
from dataclasses import dataclass
from grathon.core.TLSchema_Manager.tltypes import (
    autoDownloadSettings,
    NetworkType,
    updateOption,
    updateFileDownloads,
)


@dataclass
class DownloadStats:
    """Download statistics"""
    total_size: int = 0
    total_count: int = 0
    downloaded_size: int = 0

    @property
    def progress_percent(self) -> float:
        """Download progress percentage"""
        if self.total_size == 0:
            return 0.0
        return (self.downloaded_size / self.total_size) * 100

    def __str__(self) -> str:
        mb_total = self.total_size / (1024 * 1024)
        mb_downloaded = self.downloaded_size / (1024 * 1024)
        return (
            f"📊 Downloads: {self.total_count} files\n"
            f"   Downloaded: {mb_downloaded:.2f} MB / {mb_total:.2f} MB\n"
            f"   Progress: {self.progress_percent:.1f}%"
        )


class AutoDownloadManager:
    """Manage auto-download settings"""

    def __init__(self, client):
        """
        Initialize manager
        Args:
            client: TdClient instance
        """
        self.client = client
        self.stats = DownloadStats()
        self._on_stats_change: Optional[Callable] = None

    async def disable_all_downloads(self) -> bool:
        """Disable all auto-downloads"""
        all_ok = True
        try:
            print("🛑 Disabling all auto-downloads...")

            # نام‌های صحیح TDLib network types
            network_types = [
                ("WiFi", "networkTypeWiFi"),
                ("Mobile", "networkTypeMobile"),
                ("MobileRoaming", "networkTypeMobileRoaming"),
                ("Other", "networkTypeOther"),
            ]

            for label, td_type in network_types:
                disabled_settings = autoDownloadSettings(
                    is_auto_download_enabled=False,
                    max_photo_file_size=0,
                    max_video_file_size=0,
                    max_other_file_size=0,
                    video_upload_bitrate=0,
                    preload_large_videos=False,
                    preload_next_audio=False,
                    preload_stories=False,
                    use_less_data_for_calls=False,
                )

                result = await self.client.api.set_auto_download_settings(
                    settings=disabled_settings,
                    type={"@type": td_type},
                )

                # Check if result is an error
                td_type_str = getattr(result, "__td_type__", "")
                if td_type_str == "error" or "error" in str(result).lower()[:10]:
                    print(f"❌ {label}: {result}")
                    all_ok = False
                else:
                    print(f"✅ {label}: OK")

            return all_ok

        except Exception as e:
            print(f"❌ Error disabling downloads: {e}")
            return False

    async def set_custom_download_limits(
        self,
        network_type: str = "Mobile",
        max_photo_size: int = 0,
        max_video_size: int = 0,
        max_other_size: int = 0,
    ) -> bool:
        """تنظیم حد مخصوص دانلود برای نوع network

        Args:
            network_type: یکی از "WiFi", "Mobile", "MobileRoaming", "Other"
        """
        try:
            # Normalize network_type
            type_map = {
                "WIFI": "WiFi", "wifi": "WiFi", "WiFi": "WiFi",
                "MOBILE": "Mobile", "mobile": "Mobile", "Mobile": "Mobile",
                "ROAMING": "MobileRoaming", "MobileRoaming": "MobileRoaming",
                "OTHER": "Other", "other": "Other", "Other": "Other",
            }
            normalized = type_map.get(network_type, network_type)
            td_type = f"networkType{normalized}"

            settings = autoDownloadSettings(
                is_auto_download_enabled=max_photo_size > 0,
                max_photo_file_size=max_photo_size,
                max_video_file_size=max_video_size,
                max_other_file_size=max_other_size,
                video_upload_bitrate=0,
                preload_large_videos=False,
                preload_next_audio=False,
                preload_stories=False,
                use_less_data_for_calls=True,
            )

            result = await self.client.api.set_auto_download_settings(
                settings=settings,
                type={"@type": td_type},
            )
            print(f"✅ Download settings updated for {normalized}: {result}")
            return True

        except Exception as e:
            print(f"❌ Error setting limits: {e}")
            return False

    async def get_presets(self) -> dict:
        """دریافت preset های تنظیمات"""
        try:
            presets = await self.client.api.get_auto_download_settings_presets()
            print("📋 Auto-download Presets:")
            print(f"  🔴 Low:    {presets.low}")
            print(f"  🟡 Medium: {presets.medium}")
            print(f"  🟢 High:   {presets.high}")
            return {
                "low": presets.low,
                "medium": presets.medium,
                "high": presets.high,
            }
        except Exception as e:
            print(f"❌ Error getting presets: {e}")
            return {}

    def on_stats_update(self, callback: Callable) -> None:
        """زمانی که stats تغییر کند callback رو صدا بزن"""
        self._on_stats_change = callback

    async def handle_update(self, update) -> None:
        """رصد کردن updates"""

        # updateFileDownloads - تغییرات download list
        if isinstance(update, updateFileDownloads):
            self.stats.total_size = update.total_size or 0
            self.stats.total_count = update.total_count or 0
            self.stats.downloaded_size = update.downloaded_size or 0

            print(f"\n📥 Download Update:\n{self.stats}")

            if self._on_stats_change:
                await self._on_stats_change(self.stats)

        # updateOption - تغییرات تنظیمات
        elif isinstance(update, updateOption):
            if "download" in (update.name or "").lower():
                print(f"\n⚙️ Option Changed: {update.name} = {update.value}")

    def get_stats(self) -> DownloadStats:
        """دریافت آمار فعلی"""
        return self.stats
