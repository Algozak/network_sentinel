from manuf import manuf

class VendorLookup:
    _parser = manuf.MacParser()

    @staticmethod
    def get_vendor(mac: str) -> str:
        if not mac or mac == "Unknown":
            return "Unknown Device"
        
        result = VendorLookup._parser.get_manuf(mac)
        return result if result else "Unknown Vendor"
