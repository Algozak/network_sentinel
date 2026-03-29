class VendorLookup:
    # База популярных производителей (первые 6 символов MAC-адреса)
    OUI_DB = {
        "00:50:56": "VMware",
        "08:00:27": "Oracle (VirtualBox)",
        "00:15:5D": "Microsoft (Hyper-V)",
        "BC:5F:F4": "ASRock",
        "00:E0:4C": "Realtek",
        "E4:5F:01": "Raspberry Pi",
        "00:1A:11": "Google",
        "D8:47:32": "TP-Link",
        "AC:AF:B9": "Xiaomi",
    }

    @staticmethod
    def get_vendor(mac: str) -> str:
        if not mac or mac == "Unknown":
            return "Unknown Device"
        
        # Берем первые 8 символов (XX:XX:XX)
        prefix = mac.upper()[:8]
        return VendorLookup.OUI_DB.get(prefix, "Generic Vendor")
