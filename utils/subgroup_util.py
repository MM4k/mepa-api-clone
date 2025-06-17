class Subgroup:
    AS = "AS"
    A4 = "A4"
    A3A = "A3a"
    A3 = "A3"
    A2 = "A2"
    A1 = "A1"

    subgroups = [
        {
            "name": AS,
            "min": 0,
            "max": 2.3,
        },
        {
            "name": A4,
            "min": 2.3,
            "max": 25,
        },
        {
            "name": A3A,
            "min": 30,
            "max": 44,
        },
        {
            "name": A3,
            "min": 69,
            "max": 69,
        },
        {
            "name": A2,
            "min": 88,
            "max": 138,
        },
        {
            "name": A1,
            "min": 230,
            "max": None,
        },
    ]

    def get_subgroup(supply_voltage_in_kv: float):
        for subgroup in Subgroup.subgroups:
            if supply_voltage_in_kv >= subgroup["min"]:
                if not subgroup["max"]:
                    return subgroup["name"]

                if supply_voltage_in_kv < subgroup["max"]:
                    return subgroup["name"]

                if subgroup["min"] == subgroup["max"] and subgroup["min"] == supply_voltage_in_kv:
                    return subgroup["name"]

        raise Exception("Subgroup not found for this supply voltage")

    def get_all_subgroups():
        return Subgroup.subgroups
