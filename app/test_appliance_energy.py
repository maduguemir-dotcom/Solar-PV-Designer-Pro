# ==========================================================

# SOLAR PV DESIGNER PRO AFRICA™

# ==========================================================

#

# Appliance Energy Calculator Test

# Version: 2.4.0

#

# Developed by:

# Engr. Prof. Ibrahim Sani Madugu

#

# Purpose:

# Test the appliance_energy.py module independently

# before integration into main.py.

#

# ==========================================================

from appliance_energy import (
calculate_appliance_energy,
calculate_total_daily_energy,
calculate_monthly_energy,
calculate_annual_energy,
summarize_appliances
)

# ==========================================================

# TEST 1 - SINGLE APPLIANCE

# ==========================================================

print("\n" + "=" * 60)
print("TEST 1 - SINGLE APPLIANCE")
print("=" * 60)

fan_energy = calculate_appliance_energy(
wattage=60,
quantity=2,
hours_per_day=8
)

print(
f"Fan energy: {fan_energy:.3f} kWh/day"
)

# ==========================================================

# TEST 2 - MULTIPLE APPLIANCES

# ==========================================================

print("\n" + "=" * 60)
print("TEST 2 - MULTIPLE APPLIANCES")
print("=" * 60)

appliances = [

```
{
    "name": "Fan",
    "quantity": 2,
    "wattage": 60,
    "hours_per_day": 8
},

{
    "name": "Television",
    "quantity": 1,
    "wattage": 100,
    "hours_per_day": 5
},

{
    "name": "Refrigerator",
    "quantity": 1,
    "wattage": 150,
    "hours_per_day": 10
},

{
    "name": "LED Lights",
    "quantity": 6,
    "wattage": 10,
    "hours_per_day": 6
}
```

]

for appliance in appliances:

```
energy = calculate_appliance_energy(

    wattage=appliance["wattage"],

    quantity=appliance["quantity"],

    hours_per_day=appliance["hours_per_day"]

)

appliance["daily_energy"] = energy

print(
    f"{appliance['name']}: "
    f"{energy:.3f} kWh/day"
)
```

# ==========================================================

# TEST 3 - TOTAL DAILY ENERGY

# ==========================================================

print("\n" + "=" * 60)
print("TEST 3 - TOTAL DAILY ENERGY")
print("=" * 60)

total_daily = calculate_total_daily_energy(
appliances
)

print(
f"Total daily energy demand: "
f"{total_daily:.3f} kWh/day"
)

# ==========================================================

# TEST 4 - MONTHLY ENERGY

# ==========================================================

print("\n" + "=" * 60)
print("TEST 4 - MONTHLY ENERGY")
print("=" * 60)

monthly_energy = calculate_monthly_energy(
total_daily
)

print(
f"Estimated monthly energy: "
f"{monthly_energy:.3f} kWh/month"
)

# ==========================================================

# TEST 5 - ANNUAL ENERGY

# ==========================================================

print("\n" + "=" * 60)
print("TEST 5 - ANNUAL ENERGY")
print("=" * 60)

annual_energy = calculate_annual_energy(
total_daily
)

print(
f"Estimated annual energy: "
f"{annual_energy:.3f} kWh/year"
)

# ==========================================================

# TEST 6 - APPLIANCE SUMMARY

# ==========================================================

print("\n" + "=" * 60)
print("TEST 6 - APPLIANCE SUMMARY")
print("=" * 60)

summary = summarize_appliances(
appliances
)

print(
f"Number of appliance types: "
f"{summary.get('appliance_count', 'N/A')}"
)

print(
f"Total daily demand: "
f"{summary.get('total_daily_energy', 'N/A')} kWh/day"
)

print(
f"Monthly demand: "
f"{summary.get('monthly_energy', 'N/A')} kWh/month"
)

print(
f"Annual demand: "
f"{summary.get('annual_energy', 'N/A')} kWh/year"
)

# ==========================================================

# TEST 7 - BASIC VALIDATION

# ==========================================================

print("\n" + "=" * 60)
print("TEST 7 - VALIDATION")
print("=" * 60)

try:

```
invalid_result = calculate_appliance_energy(

    wattage=-100,

    quantity=1,

    hours_per_day=5

)

print(
    "Negative wattage result:",
    invalid_result
)
```

except Exception as error:

```
print(
    "Negative wattage correctly rejected:",
    error
)
```

# ==========================================================

# FINAL TEST MESSAGE

# ==========================================================

print("\n" + "=" * 60)
print("APPLIANCE ENERGY MODULE TEST COMPLETED")
print("=" * 60)

print(
"\nIf all calculations completed without "
"unexpected errors, the appliance module "
"is ready for dashboard integration."
)
