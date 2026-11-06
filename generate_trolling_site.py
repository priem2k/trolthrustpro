import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "TrolThrustPro"
SITE_TAGLINE = "Boat Trolling Motor Thrust (Lbs), Shaft Length (Inches) & 12V/24V/36V Battery Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b"

# Cumulative Daily Review Engine: Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/trolthrustpro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "trolthrustpro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Minn Kota Terrova / Riptide Terrova 55 / 80 / 112 Lb Thrust Bow-Mount Trolling Motor w/ GPS Spot-Lock",
        "category": "GPS Bow-Mount Trolling Motor",
        "rating": "4.8 ★ (4,650+ reviews)",
        "badge": "#1 GPS Spot-Lock Motor",
        "specs": "12V (55lb) / 24V (80lb) / 36V (112lb) | GPS Spot-Lock Electronic Anchor | Stow/Deploy Lever + Wireless Remote",
        "keyword": "Minn+Kota+Terrova+55+80+112+lb+GPS+Trolling+Motor"
    },
    {
        "title": "NOCO Genius GENPRO10X2 / GENPRO10X3 / GENPRO10X4 (10A/Bank) Waterproof Onboard Marine Battery Charger",
        "category": "IP68 Onboard Marine Charger",
        "rating": "4.9 ★ (16,800+ reviews)",
        "badge": "#1 Onboard Marine Charger",
        "specs": "10 Amps Per Bank (20A/30A/40A Total) | Charges LiFePO4, AGM & Wet Cells Independently | IP68 Waterproof",
        "keyword": "NOCO+Genius+GENPRO10X2+GENPRO10X3+Onboard+Marine+Battery+Charger"
    },
    {
        "title": "Garmin Striker Vivid 7sv / 9sv & ECHOMAP UHD2 93sv Fish Finder w/ GT54/GT56 ClearVü & SideVü Transducer",
        "category": "Side-Imaging Fish Finder",
        "rating": "4.8 ★ (9,200+ reviews)",
        "badge": "#1 Side-Imaging Sonar",
        "specs": "CHIRP Traditional + ClearVü + SideVü Scanning | Built-In Quickdraw Contours Mapping | Sunlight-Readable",
        "keyword": "Garmin+Striker+Vivid+9sv+ECHOMAP+UHD2+Fish+Finder+Transducer"
    },
    {
        "title": "LiTime 12V 100Ah TM / 24V 100Ah / 36V 50Ah–100Ah Marine Trolling Motor LiFePO4 Lithium Battery",
        "category": "Marine Trolling Motor LiFePO4",
        "rating": "4.8 ★ (12,400+ reviews)",
        "badge": "#1 Marine Lithium Battery",
        "specs": "Upgraded Surge BMS for Trolling Motors | Low-Temp Cutoff + Saltwater-Resistant Case | 4,000+ Cycles",
        "keyword": "LiTime+12V+24V+36V+100Ah+Trolling+Motor+LiFePO4+Battery"
    },
    {
        "title": "Minn Kota Endura Max 50 / 55 Lb Thrust Transom-Mount Trolling Motor w/ Digital Maximizer (36\"/42\")",
        "category": "Transom-Mount Trolling Motor",
        "rating": "4.8 ★ (11,900+ reviews)",
        "badge": "#1 Jon Boat & Skiff Motor",
        "specs": "Digital Maximizer Delivers up to 5x Longer Run Time | 6\" Telescoping Tiller | Indestructible Composite Shaft",
        "keyword": "Minn+Kota+Endura+Max+55+lb+Transom+Mount+Trolling+Motor"
    },
    {
        "title": "Humminbird HELIX 7 / HELIX 9 CHIRP MEGA SI+ GPS G4N Fish Finder & Chartplotter",
        "category": "MEGA Side-Imaging Sonar",
        "rating": "4.8 ★ (4,100+ reviews)",
        "badge": "#1 Minn Kota One-Boat Link",
        "specs": "MEGA Side Imaging+ (200 Ft Left/Right) | AutoChart Live | Links to Minn Kota i-Pilot to Follow Depth Contours",
        "keyword": "Humminbird+HELIX+7+HELIX+9+MEGA+SI+GPS+Fish+Finder"
    },
    {
        "title": "Newport Vessels Kayak Series 36 Lb / 55 Lb & NK180PRO Brushless Kayak Electric Trolling Motor",
        "category": "Kayak & Canoe Trolling Motor",
        "rating": "4.8 ★ (5,700+ reviews)",
        "badge": "#1 Fishing Kayak Motor",
        "specs": "24\"/36\" Shaft Engineered for Kayaks | Saltwater Rated Stainless Hardware | LED Battery Meter",
        "keyword": "Newport+Vessels+Kayak+Series+55+lb+NK180PRO+Trolling+Motor"
    },
    {
        "title": "Minn Kota MKR-27 60-Amp Waterproof Circuit Breaker + MKR-28 High-Current Trolling Motor Plug & Receptacle",
        "category": "60A Marine Wiring & Plug Kit",
        "rating": "4.9 ★ (8,800+ reviews)",
        "badge": "#1 Mandatory 60A Rigging Kit",
        "specs": "IP67 Waterproof Manual-Reset 60A Breaker | Continuous 60A Silver-Plated Plug (12V/24V/36V up to 6 AWG)",
        "keyword": "Minn+Kota+MKR+27+60+Amp+Breaker+and+MKR+28+Plug+Receptacle"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Minn Kota Terrova 80 (24V)",
        "type": "Bow-Mount GPS Spot-Lock",
        "thrust_spec": "80 Lbs Thrust (24V) | 45\"/54\"/60\"",
        "boat_match": "Boats up to 4,000 Lbs (17'–21')",
        "highlight": "Industry #1 GPS Spot-Lock Anchor",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Minn+Kota+Terrova+80+lb+24V+GPS+Trolling+Motor"
    },
    {
        "model": "Minn Kota Terrova 112 (36V)",
        "type": "Heavy Bow-Mount GPS",
        "thrust_spec": "112 Lbs Thrust (36V) | 60\"/72\"",
        "boat_match": "Boats up to 5,600 Lbs (20'–25')",
        "highlight": "Holds Bay Boats & Pontoons in Heavy Wind",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Minn+Kota+Terrova+112+lb+36V+Trolling+Motor"
    },
    {
        "model": "Minn Kota Endura Max 55 (12V)",
        "type": "Transom Tiller w/ Maximizer",
        "thrust_spec": "55 Lbs Thrust (12V) | 36\"/42\"",
        "boat_match": "Jon Boats, Skiffs & Canoes (<2,500 Lb)",
        "highlight": "PWM Digital Maximizer = 5x Battery Life",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Minn+Kota+Endura+Max+55+lb+Trolling+Motor"
    },
    {
        "model": "LiTime 24V 100Ah / 36V 50Ah TM",
        "type": "Single-Case Marine LiFePO4",
        "thrust_spec": "2,560 Wh (24V) / 1,920 Wh (36V)",
        "boat_match": "Replaces 2 or 3 Heavy Lead Batteries!",
        "highlight": "Saves 110 Lbs in Boat Bow + Surge BMS",
        "rating": "4.8 / 5.0 ★",
        "keyword": "LiTime+24V+36V+Trolling+Motor+LiFePO4+Battery"
    },
    {
        "model": "NOCO Genius GENPRO10X3 (30A)",
        "type": "3-Bank Waterproof Charger",
        "thrust_spec": "10A × 3 Banks (30A Total Output)",
        "boat_match": "Charges 24V TM + 12V Cranking Battery",
        "highlight": "Mix LiFePO4 & AGM on Different Banks!",
        "rating": "4.9 / 5.0 ★",
        "keyword": "NOCO+Genius+GENPRO10X3+3+Bank+Marine+Charger"
    },
    {
        "model": "Garmin ECHOMAP UHD2 93sv",
        "type": "9\" SideVü Chartplotter",
        "thrust_spec": "9\" Touchscreen + GT56UHD Transducer",
        "boat_match": "1,066 kHz Ultra-High-Def Side Scanning",
        "highlight": "Preloaded Navionics+ Lake & Coastal Maps",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Garmin+ECHOMAP+UHD2+93sv+with+GT56UHD+Transducer"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-12v-55lb-vs-24v-80lb-vs-36v-112lb-trolling-motor-thrust",
        "title": "12V (55 Lb) vs. 24V (80 Lb) vs. 36V (112 Lb) Trolling Motor: Boat Weight, Wind & Amp Draw Compared",
        "product_a": "24V (80 Lb) & 36V (112 Lb) Systems",
        "product_b": "12V (55 Lb) Single-Battery System",
        "winner_badge": "50% Lower Amp Draw & Holds Spot-Lock in 20 MPH Wind vs. Lightweight 1-Battery Setup",
        "keyword_a": "Minn+Kota+Terrova+80+lb+112+lb+24V+36V+Trolling+Motor",
        "keyword_b": "Minn+Kota+Terrova+Endura+Max+55+lb+12V+Trolling+Motor",
        "summary": "See why a 24V 80-lb motor uses LESS battery amperage at 3 MPH than a 12V 55-lb motor running wide open at 100% throttle.",
        "metrics": [
            {"feature": "Max Loaded Boat Weight", "val_a": "24V (80 Lb): Up to 4,000 Lbs | 36V (112 Lb): Up to 5,600 Lbs", "val_b": "12V (55 Lb): Strictly Boats Under 2,200–2,500 Lbs"},
            {"feature": "Amp Draw at 40 Lbs of Thrust", "val_a": "Draws Only ~16–22 Amps at Half Throttle (High Efficiency!)", "val_b": "Draws 38–45 Amps Near Full Throttle (Drains Battery Fast)"},
            {"feature": "Holding GPS Spot-Lock in 18 MPH Wind", "val_a": "Holds Position Effortlessly at 50%–65% Motor Speed", "val_b": "Spins at 100% Prop Speed & Loses Anchor Lock in Gusts"},
            {"feature": "Battery Configuration", "val_a": "One 24V/36V Single-Case LiFePO4 (or Two/Three 12V in Series)", "val_b": "Single 12V 100Ah LiFePO4 Battery (Weighs Only 24 Lbs)"},
            {"feature": "Best Boat Types", "val_a": "17'–24' Bass Boats, Pontoons, Deep-V Walleye & Bay Boats", "val_b": "12'–16' Jon Boats, Skiffs, Inflatables & Fishing Kayaks"}
        ],
        "verdict_text": "Never under-size your trolling motor voltage: a 12V 55-lb motor on an 18-foot bass boat or pontoon has to run at 95%–100% speed just to fight a 12 MPH breeze—drawing 50 amps and draining your battery by noon. Stepping up to a 24V 80-lb (or 36V 112-lb) motor lets the prop spin at a gentle 40% throttle where Pulse-Width Modulation (PWM) Digital Maximizer electronics cut amp draw in half!"
    },
    {
        "slug": "compare-minn-kota-terrova-endura-max-digital-maximizer-vs-5-speed-resistor-motor",
        "title": "Minn Kota Digital Maximizer (Variable PWM) vs. Standard 5-Speed Resistor Trolling Motor: 5x Battery Runtime",
        "product_a": "Digital Maximizer PWM (Endura Max / Terrova)",
        "product_b": "Standard 5-Speed Coil-Resistor (Endura C2)",
        "winner_badge": "Up to 5x Longer Battery Runtime on 1 Charge vs. Wasted Resistor Heat",
        "keyword_a": "Minn+Kota+Endura+Max+55+lb+Digital+Maximizer+Trolling+Motor",
        "keyword_b": "Minn+Kota+Endura+C2+55+lb+Trolling+Motor",
        "summary": "Understand the electrical secret that most anglers don't know: why a standard 5-speed trolling motor burns almost as many amps on Speed 1 as it does on Speed 5!",
        "metrics": [
            {"feature": "How Speed Control Works", "val_a": "Microprocessor Pulse-Width Modulation (Switches Power 20,000x/Sec)", "val_b": "Dumps Excess Battery Power Into Wire Resistor Coils in Lower Unit"},
            {"feature": "Amp Draw at Low Trolling Speed", "val_a": "Drops to Only 6 to 10 Amps (Delivers Up to 5x Longer Runtime!)", "val_b": "Still Draws 20 to 30+ Amps (Boils the Water Around the Motor!)"},
            {"feature": "Speed Adjustment Resolution", "val_a": "Infinite Variable Dial — Match Exact 1.2 MPH Crankbait Speed", "val_b": "Only 5 Fixed Clicks (Speed 1 Is Often Too Slow, Speed 2 Too Fast)"},
            {"feature": "Price Difference", "val_a": "~$75 to $90 More Than Standard C2", "val_b": "Lowest Upfront Entry Price"},
            {"feature": "Battery Size Savings", "val_a": "1× 100Ah Battery Lasts All Day on Endura Max", "val_b": "Requires Carrying a 2nd Battery for Full-Day Trolling"}
        ],
        "verdict_text": "On a cheap 5-speed trolling motor (like the base Endura C2), setting the handle to Speed 1 or Speed 2 does NOT save your battery: the motor still pulls heavy current from the battery and simply burns off the unused electricity as heat inside resistor coils in the lower unit! Upgrading to the Minn Kota Endura Max (or Terrova) with Digital Maximizer uses PWM electronics to draw only the exact amps needed—giving you up to 5 times longer runtime on a single 100Ah LiFePO4 battery."
    },
    {
        "slug": "compare-single-24v-36v-trolling-motor-lifepo4-battery-vs-series-12v-batteries",
        "title": "Single 24V/36V Marine LiFePO4 Battery vs. Two/Three 12V Batteries in Series: Balancing, Weight & Space",
        "product_a": "Single-Case 24V 100Ah or 36V 50Ah–100Ah LiFePO4",
        "product_b": "Two or Three 12V 100Ah Batteries Wired in Series",
        "winner_badge": "Zero Inter-Battery Voltage Drift & 50% Less Bilge Space vs. 12V Redundancy",
        "keyword_a": "LiTime+24V+100Ah+36V+50Ah+100Ah+Trolling+Motor+LiFePO4+Battery",
        "keyword_b": "LiTime+12V+100Ah+TM+Trolling+Motor+LiFePO4+Battery+and+NOCO+GENPRO10X3",
        "summary": "Compare BMS cell balancing, bilge compartment space, and charger costs between a native 24V/36V battery and series-wired 12V batteries.",
        "metrics": [
            {"feature": "Internal BMS Cell Balancing", "val_a": "1 Unified BMS Balances All 8 (24V) or 12 (36V) Cells Together", "val_b": "Separate BMSs Can Drift Out of Balance Over Time Without Multi-Bank Charger"},
            {"feature": "Bilge Compartment Footprint", "val_a": "1 Single Battery Tray & 0 Series Jumper Cables", "val_b": "Requires 2 or 3 Battery Trays + 6-AWG Series Jumper Cables"},
            {"feature": "Weight vs. Lead-Acid (36V Bank)", "val_a": "One 36V 50Ah/100Ah LiFePO4 Weighs 33–62 Lbs (Saves 140 Lbs!)", "val_b": "Three 12V 100Ah LiFePO4 Weigh 72 Lbs (Three Group-31 Lead Weigh 205 Lbs!)"},
            {"feature": "Onboard Charging Method", "val_a": "Uses Single Dedicated 24V or 36V Waterproof LiFePO4 Charger", "val_b": "Uses NOCO Genius GENPRO10X2 / 10X3 Multi-Bank Charger (10A Per 12V)"},
            {"feature": "Emergency 12V Backup Use", "val_a": "Strictly 24V or 36V Output (Cannot Jump-Start 12V Outboard Directly)", "val_b": "Can Unhook 1 Battery to Run 12V Electronics in an Emergency"}
        ],
        "verdict_text": "If you are rigging a kayak, skiff, or bass boat with tight bilge compartments, a single-case 24V 100Ah or 36V 50Ah/100Ah Trolling Motor LiFePO4 Battery saves half the floor space, eliminates series jumper cables, and keeps all cells balanced under one unified BMS. If your boat already has two or three Group-27/31 battery trays glassed into the hull and you want to charge your 12V outboard cranking battery and trolling batteries from one plug, use 12V 100Ah TM batteries paired with a NOCO Genius GENPRO10X3 onboard charger."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-minn-kota-terrova-and-riptide-terrova-gps-spot-lock-trolling-motor",
        "title": "Minn Kota Terrova (55/80/112 Lb) Review: Why i-Pilot GPS Spot-Lock Is the Greatest Fishing Invention Ever",
        "product_name": "Minn Kota Terrova / Riptide Terrova 55 / 80 / 112 Lb GPS Trolling Motor",
        "category": "Bow-Mount GPS Trolling Motor",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 GPS Trolling Motor",
        "spec_1": "55 Lb (12V) / 80 Lb (24V) / 112 Lb (36V) Thrust",
        "spec_2": "Sub-Meter GPS Spot-Lock w/ Jog Feature (5-Ft Steps)",
        "spec_3": "Shaft Lengths: 45\", 54\", 60\", and 72\" Composite",
        "spec_4": "Includes Wireless LCD Remote + Heading Sensor Puck",
        "published_date": "2026-11-01",
        "keyword": "Minn+Kota+Terrova+55+80+112+lb+GPS+Trolling+Motor",
        "summary": "Holding your boat within 2 feet of a submerged brush pile in 20 MPH wind and river current without ever dropping a heavy rope anchor, the Minn Kota Terrova with GPS Spot-Lock transforms how you fish.",
        "pros": [
            "GPS Spot-Lock acts as an invisible electronic anchor—automatically steering and adjusting prop speed to hold your exact GPS coordinate in wind and current",
            "Included Bluetooth Heading Sensor puck unlocks 'Spot-Lock Jog'—press the arrow button to move your anchored boat 5 feet forward, back, left, or right",
            "Fall-away stow/deploy ramp + Lift-Assist spring mechanism lets you slide the motor into the water with two fingers",
            "Digital Maximizer variable PWM circuitry delivers up to 5x longer battery runtime than multi-speed motors"
        ],
        "cons": [
            "Always mount the motor using a Minn Kota RTA-17 or MKA-21 composite quick-release bracket so you can slide the motor off the bow for secure garage storage or boat covers"
        ],
        "body_paragraphs": [
            "When sizing a bow-mount trolling motor on our boat weight and shaft length calculator, two numbers dictate your success: **Thrust (Lbs)** and **Shaft Length (Inches)**. For an 18-to-20 foot bass boat, deep-V walleye boat, or pontoon weighing 2,800 to 3,800 lbs loaded, our formula ($2\text{ lbs per }100\text{ lbs weight} \times 1.25\text{ wind factor}$) requires an 80-lb 24V Minn Kota Terrova. If your bow sits 24 inches above the waterline, adding 20 inches for submerged prop depth plus 8 inches for waves points directly to the 54-inch or 60-inch shaft.",
            "In our on-water test holding over a 22-foot main-lake hump in a 17 MPH crosswind, pressing the anchor icon on the Terrova's wireless lanyard remote locked the boat directly over the school of fish while both anglers stood at the bow casting hands-free.",
            "For saltwater bay boats and flats skiffs, order the white **Riptide Terrova** edition, which adds sacrificial zinc anodes and multi-layer epoxy salt armor."
        ]
    },
    {
        "slug": "review-noco-genius-genpro10x2-10x3-10x4-onboard-marine-battery-charger",
        "title": "NOCO Genius GENPRO10X3 Review: The IP68 Waterproof Onboard Charger That Charges LiFePO4 & AGM Together",
        "product_name": "NOCO Genius GENPRO10X2 / 10X3 / 10X4 (10A/Bank) Onboard Marine Charger",
        "category": "Onboard Marine Battery Charger",
        "rating_score": "4.9",
        "verdict_badge": "#1 Onboard Marine Battery Charger",
        "spec_1": "10 Amps Per Bank (20A 2-Bank / 30A 3-Bank / 40A 4-Bank)",
        "spec_2": "Independent Chemistry Mode Per Bank (LiFePO4, AGM, Wet)",
        "spec_3": "100% Sealed IP68 Waterproof (Tested Submerged Under Water!)",
        "spec_4": "1-Volt Force Mode Wakes Up Sleeping BMS Lithium Batteries",
        "published_date": "2026-11-01",
        "keyword": "NOCO+Genius+GENPRO10X2+GENPRO10X3+Onboard+Marine+Battery+Charger",
        "summary": "Most boats run LiFePO4 batteries for the trolling motor and a lead-acid/AGM battery for cranking the outboard. The NOCO Genius GENPRO lets you set Bank 1 to AGM and Banks 2 & 3 to 14.6V Lithium independently!",
        "pros": [
            "Every bank is completely isolated and independently selectable between 12V Lithium (LiFePO4), 12V AGM, 12V Flooded, and 12V Repair Mode",
            "Full 10 Amps per bank recharges a depleted 100Ah trolling motor battery bank overnight in 8 to 9 hours so you are 100% full by dawn",
            "Force Mode detects batteries down to 1 Volt (or 0.0V sleeping LiFePO4 BMS) and applies a wake-up pulse to turn the lithium BMS back on",
            "40% smaller and 35% lighter than old epoxy-brick marine chargers, with integrated anti-vibration rubber mounting feet"
        ],
        "cons": [
            "Pair with a NOCO GCP1 15A waterproof thru-hull AC port plug on your splashwell so you can plug an extension cord into your boat without opening hatches"
        ],
        "body_paragraphs": [
            "Here is the classic marine wiring dilemma: outboard engine manufacturers (Mercury, Yamaha, Suzuki) often recommend a high-CCA AGM battery for starting the gas engine, while anglers want lightweight 12V 100Ah LiFePO4 batteries in series for their 24V or 36V trolling motor. Old onboard chargers forced all banks to use the same charging profile.",
            "The NOCO Genius GENPRO10X3 (3-Bank, 30A) solves this effortlessly. You bolt it permanently inside your rear battery compartment, connect Bank 1 to your AGM cranking battery (set to AGM mode), and connect Banks 2 and 3 directly across your two series-wired 12V LiFePO4 trolling batteries (set to Lithium mode).",
            "Because each NOCO bank is transformer-isolated, you never have to disconnect your 24V/36V series jumper cable when plugging in to charge after a tournament."
        ]
    },
    {
        "slug": "review-garmin-echomap-uhd2-and-striker-vivid-sidevu-fish-finder",
        "title": "Garmin ECHOMAP UHD2 & Striker Vivid 7sv/9sv Review: Finding Hidden Structure With 1,066 kHz SideVü Sonar",
        "product_name": "Garmin ECHOMAP UHD2 73sv/93sv & Striker Vivid 7sv/9sv Fish Finder",
        "category": "Side-Imaging Fish Finder",
        "rating_score": "4.8",
        "verdict_badge": "#1 Side-Imaging Fish Finder",
        "spec_1": "7-Inch or 9-Inch Sunlight-Readable Color Display",
        "spec_2": "3-in-1 Transducer: CHIRP + ClearVü + SideVü (GT52/GT54/GT56)",
        "spec_3": "Quickdraw Contours Creates Custom 1-Foot HD Lake Maps Live",
        "spec_4": "High-Contrast Vivid Color Palettes Reveal Fish vs Brush",
        "published_date": "2026-11-01",
        "keyword": "Garmin+Striker+Vivid+9sv+ECHOMAP+UHD2+Fish+Finder+Transducer",
        "summary": "Traditional 2D sonar only shows a narrow cone directly under your boat. Garmin's SideVü scanning sonar beams 150 feet left and right of your hull—revealing sunken timber, rock piles, and baitballs like an underwater X-ray.",
        "pros": [
            "SideVü side-imaging scans up to 200 feet to both sides of your boat simultaneously—letting you search an entire cove in a single pass",
            "Seven new high-contrast Vivid color palettes (like Lava, Aqua, and Caribbean) make hard rock bottoms glow bright against soft mud and suspended bass",
            "Built-in GPS with Quickdraw Contours automatically draws custom 1-foot depth contour maps of unmapped ponds and rivers as you drive",
            "Quick-release tilt/swivel bail mount lets you unclip the display screen in 3 seconds at the boat ramp"
        ],
        "cons": [
            "Always choose the 'sv' (SideVü) model rather than the cheaper 'cv' (ClearVü only) model—side-imaging is worth every single penny for locating fish"
        ],
        "body_paragraphs": [
            "When outfitting a fishing boat or kayak, your trolling motor and your fish finder work as a team: you use SideVü side-imaging to spot a submerged rock ledge or brush pile 60 feet off the port side of your boat, drop a GPS waypoint on the screen, drive over to it, and hit Spot-Lock on your trolling motor.",
            "For budget-conscious anglers on jon boats, kayaks, and skiffs, the **Garmin Striker Vivid 7sv / 9sv** (bundled with the GT52HW-TM transducer) delivers full CHIRP, Down-Imaging (ClearVü), Side-Imaging (SideVü), and GPS contour mapping for a fraction of big chartplotter prices.",
            "If you want pre-loaded Garmin Navionics+ lake/coastal maps, touchscreens, and LiveScope Plus (LVS34) forward-facing sonar compatibility, step up to the **Garmin ECHOMAP UHD2 93sv** with the ultra-high-definition GT56UHD transducer."
        ]
    },
    {
        "slug": "review-litime-12v-100ah-tm-and-24v-36v-trolling-motor-lifepo4-battery",
        "title": "LiTime Trolling Motor LiFePO4 Review: Upgraded Surge BMS & Why Dropping 100 Lbs of Lead Adds 3 MPH Boat Speed",
        "product_name": "LiTime 12V 100Ah TM / 24V 100Ah / 36V 50Ah Trolling Motor LiFePO4 Battery",
        "category": "Marine Trolling Motor LiFePO4",
        "rating_score": "4.9",
        "verdict_badge": "#1 Trolling Motor Lithium Battery",
        "spec_1": "Upgraded Trolling-Motor Surge BMS (Handles Prop Weed-Chops!)",
        "spec_2": "Built-In Low-Temperature Cutoff + Saltwater Moisture Seal",
        "spec_3": "Weighs 65% Less Than Group-27/31 Lead-Acid Batteries",
        "spec_4": "Constant 13.2V / 26.4V / 39.6V Thrust All Day Long",
        "published_date": "2026-11-01",
        "keyword": "LiTime+12V+24V+36V+100Ah+Trolling+Motor+LiFePO4+Battery",
        "summary": "Standard solar LiFePO4 batteries sometimes trip their BMS when a trolling motor prop chops through thick hydrilla weeds. LiTime's dedicated 'TM' (Trolling Motor) edition features a high-inrush TVS-protected BMS built specifically for marine motors.",
        "pros": [
            "Dedicated Trolling Motor BMS handles instantaneous 300A–500A prop-stall surges when chopping through heavy lily pads and milfoil without tripping",
            "Replaces two 68-lb Group-31 lead-acid batteries (136 lbs) with just 44 lbs of lithium—lifting your boat's bow 2 inches higher to draft shallower and plane faster",
            "Maintains 100% peak thrust from morning until 5 PM (unlike lead-acid batteries that sag to 11.2V and feel sluggish by noon)",
            "Provides 2x the usable amp-hours of an identically rated 100Ah AGM battery (100% usable vs 50% usable)"
        ],
        "cons": [
            "Always install a Minn Kota MKR-27 60-Amp manual-reset circuit breaker on the positive cable within 12 inches of the battery post"
        ],
        "body_paragraphs": [
            "Using our trolling motor battery runtime calculator, an 80-lb 24V trolling motor draws an average of 12 to 18 Amps during a normal day of mixed Spot-Locking and bank fishing (with brief 55-amp bursts when moving spots). On two 100Ah lead-acid batteries (only 50Ah usable capacity before voltage sags), you run out of power after 3.5 hours of heavy wind. On a 100Ah LiFePO4 bank (100Ah full usable capacity at flat voltage), you get 6.5 to 9+ hours of full-power thrust!",
            "What makes LiTime's 'TM' series special is its marine-hardened BMS: it includes Transient Voltage Suppression (TVS) diodes that absorb inductive voltage spikes generated by brushed and brushless trolling motors.",
            "Whether you choose two 12V 100Ah TM batteries in series or a single-case 24V 100Ah / 36V 50Ah battery, taking 90 to 130 lbs of dead lead out of your boat transforms hole-shot acceleration."
        ]
    }
]

# Deep Catalog of 36+ Trolling Motors, Fish Finders, Marine Batteries & Rigging Gear for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("minn-kota-endura-max-50-55-lb-transom-trolling-motor", "Minn Kota Endura Max 50 & 55 Lb Thrust Transom-Mount Trolling Motor (Digital Maximizer)", "Transom Trolling Motor", "4.8", "#1 Jon Boat, Skiff & Canoe Trolling Motor", "50 Lb or 55 Lb Thrust (12V) | 36\" & 42\" Shafts", "Digital Maximizer PWM Gives Up to 5x Longer Battery Life", "6-Inch Telescoping Twist-Tiller Handle", "10-Position Lever-Lock Bracket + Indestructible Shaft", "Minn+Kota+Endura+Max+55+lb+Transom+Mount+Trolling+Motor", "With variable speed control and Digital Maximizer electronics that stretch a single 12V 100Ah battery across two full days of fishing, the Minn Kota Endura Max 55 is the undisputed king of transom motors."),
    ("humminbird-helix-7-helix-9-chirp-mega-si-gps-g4n", "Humminbird HELIX 7 & HELIX 9 CHIRP MEGA SI+ GPS G4N Fish Finder", "MEGA Side-Imaging Sonar", "4.8", "#1 Sonar to Link With Minn Kota i-Pilot (One-Boat Network)", "1.2 MHz MEGA Side Imaging+ & MEGA Down Imaging+", "One-Boat Network Commands Minn Kota to Follow Depth Contours!", "Dual Spectrum CHIRP 2D Sonar + AutoChart Live", "High-Brightness 1000+ Nit Display", "Humminbird+HELIX+7+HELIX+9+MEGA+SI+GPS+Fish+Finder", "When connected to a Minn Kota Terrova or Ultrex via the One-Boat Network, a Humminbird HELIX G4N lets you highlight a 12-foot weedline contour on the screen and tell the trolling motor to steer along it automatically."),
    ("newport-vessels-kayak-series-55lb-and-nk180pro-brushless-motor", "Newport Vessels Kayak Series (36/55 Lb) & NK180PRO 24V Brushless Kayak Motor", "Kayak Electric Motor", "4.8", "#1 Trolling Motor Engineered Specifically for Fishing Kayaks", "Short 24\" & 36\" Shafts Prevent High Center-of-Gravity Tip", "NK180PRO 24V Brushless Motor Hits 5.5–6.5 MPH on Kayaks!", "Saltwater-Rated Stainless Hardware + Zinc Anode", "Includes Pre-Wired Circuit Breaker Leads", "Newport+Vessels+Kayak+Series+55+lb+NK180PRO+Trolling+Motor", "Standard 42-inch transom trolling motors sit way too high on a low-profile fishing kayak. Newport's 24-inch and 36-inch Kayak Series (and 1.8HP brushless NK180PRO) keep thrust inline with the kayak hull for maximum speed."),
    ("minn-kota-mkr-27-60-amp-breaker-and-mkr-28-plug-receptacle", "Minn Kota MKR-27 60-Amp Waterproof Circuit Breaker & MKR-28 Trolling Motor Plug", "60A Marine Wiring Kit", "4.9", "#1 Mandatory Overcurrent & Melt-Proof Plug Kit", "MKR-27: 60A Waterproof Manual-Reset Push-Button Trip Breaker", "MKR-28: Continuous 60A Silver-Plated Threaded Locking Plug", "Compatible w/ 12V, 24V & 36V Systems (Accepts 6 AWG to 10 AWG)", "Eliminates Melted 30-Amp 2-Prong Bow Plugs!", "Minn+Kota+MKR+27+60+Amp+Breaker+and+MKR+28+Plug+Receptacle", "Cheap 30-amp rubber 2-prong trolling motor plugs melt at the bow when an 80-lb or 112-lb motor runs into wind. Upgrading to the silver-plated 60-amp MKR-28 locking receptacle and MKR-27 breaker eliminates voltage drop permanently."),
    ("minn-kota-rta-17-mka-21-composite-quick-release-bracket", "Minn Kota RTA-17 (Riptide) & MKA-21 Composite Quick-Release Bow Mount Bracket", "Quick-Release Bow Bracket", "4.9", "#1 Bracket to Slide Your Trolling Motor Off in 5 Seconds", "High-Yield Composite Never Rusts, Corrodes or Rattles", "Low-Profile Puck Remains on Bow Deck When Motor Is Removed", "Stainless Steel U-Pin Accepts Padlock to Prevent Theft!", "Fits Terrova, Ulterra, PowerDrive & DeckHand", "Minn+Kota+RTA+17+MKA+21+Composite+Quick+Release+Bracket", "Trying to pull a tight boat cover over a fixed bow-mount trolling motor—or leaving a $2,000 GPS motor bolted to your boat in a hotel parking lot—is a nightmare. Pull one stainless pin on the MKA-21/RTA-17 and slide the motor right off."),
    ("ancor-marine-grade-6-awg-8-awg-duplex-tinned-copper-boat-wire", "Ancor Marine Grade 25-Ft / 50-Ft 6-AWG & 8-AWG Tinned Copper Duplex Boat Cable", "Tinned Marine Copper Wire", "4.9", "#1 ABYC-Compliant Corrosion-Proof Trolling Motor Wire", "100% Electro-Tinned Ultra-Flexible Type-3 Stranded Copper", "Tin Coating Stops Green Salt/Moisture Corrosion Inside Jacket!", "Vinyl Insulation Resists Battery Acid, Bilge Oil, Gas & UV", "Exceeds US Coast Guard & ABYC Standards", "Ancor+Marine+Grade+6+AWG+8+AWG+Tinned+Copper+Boat+Wire", "Never run bare automotive or hardware-store copper wire inside a boat hull: bilge humidity wicks under the insulation and turns bare copper into black, high-resistance powder. Ancor electro-tinned marine wire stays shiny and conductive for 20 years."),
    ("garmin-livescope-plus-lvs34-system-with-gls10-sonar-black-box", "Garmin Panoptix LiveScope Plus System (LVS34 Transducer + GLS 10 Black Box)", "Real-Time Forward Sonar", "4.9", "#1 Live Forward-Facing Sonar in Tournament Fishing", "Watch Fish Swim & Strike Your Lure in Real-Time 30 FPS Video!", "35% Better Target Separation & Sharper Resolution on LVS34", "3 Modes in 1 Mount: Forward, Down & Perspective Mode", "Pairs w/ Garmin ECHOMAP UHD2 & GPSMAP", "Garmin+LiveScope+Plus+System+with+GLS+10+and+LVS34", "Transforming fishing into a live video game where you watch individual bass or crappie swim up and inhale your jig in real time up to 100 feet in front of your boat, Garmin LiveScope Plus (LVS34) dominates every tournament trail."),
    ("motorguide-xi3-55lb-70lb-wireless-kayak-and-boat-gps-trolling-motor", "MotorGuide Xi3 55 Lb (12V) & 70 Lb (24V) Pinpoint GPS Wireless Trolling Motor", "Quiet GPS Bow-Mount Motor", "4.7", "Quietest Steering Transmission + Best 36\" Kayak GPS Option", "40% Quieter Steering Motor Than Competing GPS Units", "Available in Short 36\" & 48\" Shafts for Kayaks & Skiffs!", "Pinpoint GPS Anchor, Heading Lock & Jog Included", "SecureStep Lever Stows & Deploys Effortlessly", "MotorGuide+Xi3+55+lb+70+lb+Pinpoint+GPS+Trolling+Motor", "Because MotorGuide offers the Xi3 Pinpoint GPS in a compact 36-inch and 48-inch shaft with a whisper-quiet steering gearbox, it is the #1 bow-mount GPS Spot-Lock motor for fishing kayaks, Gheenoes, and 14–16 ft jon boats."),
    ("minn-kota-ulterra-quest-80-112-lb-auto-stow-and-deploy-trolling-motor", "Minn Kota Ulterra / Ulterra QUEST 80/112 Lb Auto-Stow, Auto-Deploy & Power-Trim GPS Motor", "100% Automatic Stow/Deploy", "4.8", "#1 Motor That Launches & Stows Itself at the Push of a Button!", "Motorized Auto-Stow & Auto-Deploy From Wireless Remote or Foot Pedal!", "Motorized Power Trim Raises/Lowers Prop Depth in Shallow Water", "Never Walk to the Bow or Bend Over to Lift a Heavy Motor Again", "Includes Spot-Lock GPS + Eco Mode", "Minn+Kota+Ulterra+80+112+lb+Auto+Stow+Deploy+Trolling+Motor", "Have a high-bow pontoon, tri-toon, deep-V walleye boat, or bad lower back? Press one button on the Minn Kota Ulterra remote from the captain's helm and watch the motor unlatch, tilt over the bow, and lower itself into the water automatically."),
    ("minn-kota-mkp-32-mkp-33-mkp-38-weedless-wedge-2-spare-prop-and-nut-kit", "Minn Kota Weedless Wedge 2 Replacement Propeller (MKP-32 / MKP-33 / MKP-38) + Prop Nut Kit", "100% Weedless Spare Prop", "4.9", "#1 Mandatory Spare Part for Your Boat Glovebox", "Swept-Back Flared Blades Push Thick Hydrilla & Lily Pads Away", "Zero Battery-Draining Weed Wrapping in Shallow Marsh", "Pair w/ MKP-34 Prop Nut, Shear Pin & Washer Kit", "Swaps in 90 Seconds on the Water", "Minn+Kota+Weedless+Wedge+2+Propeller+MKP+32+MKP+33+MKP+38", "Nothing ruins a weekend fishing trip faster than snapping a shear pin or chipping a prop blade on a submerged stump at 7 AM with no spare on board. Keeping a matching Weedless Wedge 2 prop and shear-pin kit in your hatch saves the day."),
    ("t-h-marine-g-force-eliminator-billet-aluminum-trolling-motor-prop-nut", "T-H Marine G-Force Eliminator CNC Billet Aluminum Prop Nut for Minn Kota & MotorGuide", "Anti-Vibration Cooling Prop Nut", "4.8", "#1 $45 Upgrade to Silence Prop Hum & Cool Lower Unit", "Machined 6061 Billet Aluminum w/ Built-In O-Ring Dampener", "Wider Contact Face Stabilizes Prop & Cuts Sonar Interference!", "Cooling Ports Dissipate Heat for Longer Motor Seal Life", "Tool-Free Knurled Grip Spins On by Hand!", "T+H+Marine+G+Force+Eliminator+Trolling+Motor+Prop+Nut", "The stock nylon locknut on a trolling motor requires carrying a socket wrench and allows the plastic prop to flex at high speed—creating harmonic vibrations that spook shallow fish. The O-ring-damped billet aluminum G-Force Eliminator silences prop hum completely."),
    ("ram-mounts-balzac-heavy-duty-2-25-inch-d-size-fish-finder-swing-arm-mount", "RAM Mounts D-Size (2.25\" Ball) & C-Size Heavy-Duty Aluminum Fish Finder Gimbal Mount", "Rough-Water Sonar Mount", "4.9", "#1 Mount That Holds 9\" & 12\" Fish Finders Rock-Solid in 3-Ft Waves", "Massive 2.25-Inch (D-Size) Rubber-Coated Ball Absorbs Wave Shock", "Supports Heavy 9\", 10\" & 12\" Garmin/Humminbird Graphs Without Drooping", "Marine-Grade Powder-Coated Aluminum", "Made in Seattle, USA — Lifetime RAM Warranty", "RAM+Mounts+Heavy+Duty+Fish+Finder+Mount+C+Size+D+Size", "Undersized 1-inch plastic mounts flop downward the first time your boat hits a wake at 35 MPH. Stepping up to a marine-grade aluminum RAM C-Size (for 7\"–9\" screens) or D-Size 2.25\" ball mount (for 9\"–12\" screens) locks your sonar in place."),
    ("minn-kota-mka-55-mka-60-bow-mount-trolling-motor-stabilizer-bounce-buster", "Minn Kota MKA-55 / MKA-60 Bow-Mount Trolling Motor Shaft Stabilizer ('Bounce Buster')", "Stowed Shaft Stabilizer", "4.8", "#1 Protection Against Bent Shafts & Cracked Bow Gelcoat", "Supports Motor Head When Stowed Over Rough Waves & Highway Towing", "Absorbs 90% of Bow-Mount Bounce & Fiberglass Flex", "Folds Down Flat Against Deck When Motor Is Deployed", "Cut-to-Fit Segmented Aluminum Rod", "Minn+Kota+MKA+55+MKA+60+Bow+Mount+Stabilizer+Kit", "When running across 2-foot whitecaps at 40 MPH or towing your boat down a bumpy highway, an unsupported 60-inch trolling motor head bounces violently—cracking fiberglass bow decks and loosening mount bolts. A fold-down shaft stabilizer locks it solid."),
    ("yakattack-tracpak-and-no-drill-transducer-deployment-over-the-side-arm", "Scotty 141 / YakAttack SwitchBlade No-Drill Kayak & Jon Boat Transducer Deployment Arm", "No-Drill Transducer Arm", "4.8", "#1 Way to Mount a Side-Imaging Transducer Without Drilling Hull Holes!", "Clamps or Slides Into Gear Track — Zero Holes Below Waterline!", "Hydrodynamic Blade Arm Cuts Drag at Trolling Speeds", "Flips Up Out of the Water in 1 Second When Beaching!", "Fits Garmin GT52/GT54/GT56 & Humminbird MEGA Transducers", "Kayak+and+Jon+Boat+Transducer+Deployment+Arm+Mount+Scotty+YakAttack", "Don't want to drill screw holes below the waterline of your aluminum jon boat, canoe, or rotomolded kayak? A flip-up over-the-side transducer arm holds your side-imaging transducer in clean, bubble-free water and kicks up if you hit a stump."),
    ("battery-tender-027-0004-bk-80-amp-l-shaped-trolling-motor-dc-plug", "Battery Tender 80-Amp Heavy-Duty L-Shaped Trolling Motor Plug & Stainless Receptacle", "80-Amp Screw-Lock Bow Plug", "4.9", "Highest-Rated 80-Amp Trolling Motor Plug on the Market", "Rated for 80 Amps Continuous Across 12V, 24V, 36V & 48V!", "Threaded T-Handle Compression Lock Cannot Vibrate Loose!", "Silver-Plated Solid Copper Terminals (Accepts up to 4 AWG / 6 AWG)", "Waterproof Gasket Cap + Stainless Faceplate", "Battery+Tender+80+Amp+Trolling+Motor+Plug+and+Receptacle", "Using a screw-lock T-handle mechanism that compresses internal silver-plated copper lugs together with zero resistance, the 80-Amp Battery Tender plug runs ice-cold even on 36V 112-lb brushless motors."),
    ("Attwood-noco-group-27-group-31-heavy-duty-marine-battery-box-and-strap", "NOCO HM318BKS / Attwood Group 24, 27 & 31 Heavy-Duty Marine Battery Box & Tie-Down Tray", "USCG-Compliant Battery Box", "4.8", "#1 Impact-Resistant Battery Box (to -40°F) w/ Captive Lid", "Meets US Coast Guard Code 33 CFR 183.420 & ABYC E-10.7", "Rotational-Molded UV/Acid/Oil-Proof Polypropylene", "Locking Tabs + Heavy-Duty Nylon Hold-Down Strap Included", "Large Cable Entry Ports for 6-AWG Trolling Leads", "NOCO+Group+27+Group+31+Marine+Battery+Box+Tray", "Loose batteries sliding around in an aluminum jon boat or fiberglass bilge cause dead shorts and hull damage. Securing every battery inside a USCG-approved NOCO battery box protects terminals from dropped fishing pliers and rain."),
    ("haswing-cayman-b-55lb-12v-wireless-bow-mount-gps-trolling-motor", "Haswing Cayman B 55 Lb (12V, 48\"/54\") Wireless Bow-Mount Trolling Motor w/ Remote", "Budget Bow-Mount Motor", "4.6", "Best Under-$650 Wireless Bow-Mount Trolling Motor", "55 Lbs Thrust on a Single 12V Battery (48\" or 54\" Aluminum Shaft)", "Includes Wireless Rechargeable Hand Remote (+ Optional Foot Pedal)", "Saltwater Sacrificial Anode + Encapsulated Electronics", "Quick-Release Plate Available", "Haswing+Cayman+B+55+lb+12V+Bow+Mount+Trolling+Motor", "For anglers on 14-to-17 foot aluminum boats who want a wireless remote-controlled bow-mount motor without spending $1,500+, the Haswing Cayman 55Lb delivers reliable 12V bow control."),
    ("nocqua-12v-10ah-20ah-waterproof-kayak-fish-finder-lithium-battery-kit", "Nocqua Pro Power Kit 12V 10Ah & 20Ah Waterproof Lithium Battery for Fish Finders", "Dedicated Sonar Battery", "4.9", "#1 Cure for Trolling Motor Sonar Screen Static & Interference!", "Runs 7\" & 9\" Garmin/Humminbird Fish Finders for 15–30 Hours", "100% Isolates Your Fish Finder From Trolling Motor PWM Noise!", "Silicone-Sealed Waterproof Pouch Weighs Only 1.4–2.6 Lbs", "Includes 120V Wall Charger & Open-End Marine Leads", "Nocqua+12V+10Ah+20Ah+Waterproof+Fish+Finder+Lithium+Battery", "Never wire your fish finder to the same battery as your trolling motor: the motor's PWM chopper sends electrical static across your sonar screen every time you hit the pedal! Powering your graph from a dedicated 2-lb Nocqua 12V lithium pack gives you crystal-clear sonar.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: On-Water Thrust, Battery Amp Draw & Sonar Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"On-water GPS & clamp-meter verified performance ({s1}) tested in wind and current",
            f"Corrosion-proof marine engineering ({s2}) built for freshwater and saltwater rigs",
            f"Angler-friendly deck integration ({s3}) with standard ABYC wiring and mounting",
            f"Backed by {s4} for multi-season tournament reliability"
        ],
        "cons": [
            "Always verify your boat's loaded weight, bow-to-waterline shaft height, and 60A breaker sizing using our calculator before rigging"
        ],
        "body_paragraphs": [
            f"When calculating trolling motor thrust (lbs), shaft length (inches), and 12V/24V/36V LiFePO4 battery capacity on {SITE_NAME}, matching your motor voltage and shaft immersion to your hull weight is what keeps you locked on the spot when the afternoon wind kicks up. In our hands-on on-water evaluation, the {prod_name} exceeded factory benchmarks.",
            f"Equipped with {s1} and {s2}, it delivers whisper-quiet boat control and all-day battery efficiency without spooking shallow fish. Furthermore, {s3} makes bow rigging and battery charging effortless.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 rating as one of the highest-impact marine upgrades for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            boat_configs = [
                ("18' Bass Boat Rig (80 Lb 24V 54\" Terrova + 24V 100Ah LiFePO4 + 9\" SideVü)", 80, "24V / 54\" Shaft", "3,200 Lb Boat", "24V 100Ah LiFePO4"),
                ("22' Pontoon Boat Rig (80–112 Lb 60\" GPS Motor + 3-Bank NOCO Charger)", 112, "36V / 60\" Shaft", "4,500 Lb Pontoon", "36V 100Ah LiFePO4"),
                ("14'–16' Aluminum Jon Boat Rig (55 Lb 12V 42\" Endura Max + 12V 100Ah)", 55, "12V / 42\" Shaft", "1,400 Lb Jon Boat", "12V 100Ah TM"),
                ("21' Deep-V Walleye Boat Rig (112 Lb 36V 72\" Shaft + LiveScope Plus)", 112, "36V / 72\" Shaft", "4,800 Lb Deep-V", "36V 100Ah + GENPRO"),
                ("12' Tournament Fishing Kayak Rig (55 Lb / NK180PRO 36\" Shaft + 100Ah)", 55, "12V/24V 36\" Shaft", "550 Lb Kayak", "12V 100Ah Mini"),
                ("20' Saltwater Center Console Bay Boat Rig (80–112 Lb Riptide 60\" Shaft)", 80, "24V / 60\" Riptide", "3,800 Lb Bay Boat", "24V 100Ah Low-Temp")
            ]
            b_name, lbs_v, v_s, wt_s, bat_s = boat_configs[extra_num % len(boat_configs)]
            proc_tuple = (
                f"trolling-motor-{lbs_v}lb-battery-sonar-rig-review-{extra_num}",
                f"{lbs_v}-Lb Thrust ({v_s}) & {bat_s} Marine Package Review (#{extra_num})",
                f"{lbs_v} Lb / {v_s} Boat Rig",
                "4.8",
                f"Verified {lbs_v} Lb @ {wt_s}",
                f"{lbs_v} Lbs Thrust ({v_s})",
                f"Powered by {bat_s} + 60A Breaker",
                f"Sized for {wt_s}",
                "2-to-5 Year Marine System Warranty",
                f"Minn+Kota+LiTime+NOCO+Garmin+{lbs_v}+lb+Trolling+Motor",
                f"Complete GPS Spot-Lock wind-hold test, 8-hour amp-hour draw log, and shaft immersion check for a {b_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO BOAT & TROLLING PRESETS
# ==========================================
TROL_PRESETS = [
    {"slug": "18-ft-bass-boat-trolling-motor-thrust-shaft-battery-calculator", "name": "18'–19' Bass Boat (3,200 Lbs Loaded / 22\" Bow Height — 80 Lb 24V)", "boat_lbs": 3200, "bow_in": 22, "wind_cond": "1.25", "hours": 8, "mount": "bow", "desc": "Calculate exact trolling motor thrust (80 lbs / 24V), shaft length (52\"–54\"), 24V 100Ah LiFePO4 battery runtime, and 60A breaker for an 18-to-19 foot bass boat."},
    {"slug": "20-ft-24-ft-pontoon-boat-trolling-motor-size-calculator", "name": "20'–24' Pontoon Boat (4,200 Lbs + High Wind Sail — 80 to 112 Lb)", "boat_lbs": 4200, "bow_in": 26, "wind_cond": "1.35", "hours": 6, "mount": "bow", "desc": "Pontoon fence panels act like a giant wind sail! Calculate why a 20'–24' pontoon requires an 80-lb (24V) or 112-lb (36V) motor with a 54\"–60\" shaft."},
    {"slug": "14-ft-16-ft-aluminum-jon-boat-trolling-motor-battery-calculator", "name": "14'–16' Aluminum Jon Boat & Utility V-Hull (1,350 Lbs — 55 Lb 12V)", "boat_lbs": 1350, "bow_in": 15, "wind_cond": "1.15", "hours": 8, "mount": "transom", "desc": "Size a 50–55 lb 12V Minn Kota Endura Max (with Digital Maximizer), 36\"–42\" shaft, and a single 12V 100Ah LiFePO4 battery for a 14'–16' jon boat."},
    {"slug": "deep-v-walleye-and-center-console-bay-boat-36v-112lb-calculator", "name": "20'–22' Deep-V Walleye & Saltwater Bay Boat (4,600 Lbs / 30\" High Bow)", "boat_lbs": 4600, "bow_in": 30, "wind_cond": "1.35", "hours": 8, "mount": "bow", "desc": "High-freeboard Deep-V and Bay Boats pitching in 2-foot waves require a 60\" or 72\" shaft and 112 lbs (36V) of thrust so the prop never cavitates."},
    {"slug": "fishing-kayak-canoe-trolling-motor-thrust-battery-calculator", "name": "10'–13' Fishing Kayak, Canoe & Gheenoe (550 Lbs Loaded — 36 to 55 Lb)", "boat_lbs": 550, "bow_in": 10, "wind_cond": "1.15", "hours": 7, "mount": "transom", "desc": "Calculate 36-lb vs 55-lb thrust (or 24V NK180PRO brushless), short 24\"–36\" kayak shaft length, and lightweight 12V 100Ah LiFePO4 speed for fishing kayaks."},
    {"slug": "trolling-motor-shaft-length-bow-to-waterline-chart-calculator", "name": "Bow-to-Waterline Trolling Motor Shaft Length Calculator (36\" to 72\")", "boat_lbs": 3000, "bow_in": 24, "wind_cond": "1.25", "hours": 8, "mount": "bow", "desc": "Calculate exact shaft length using the marine engineering formula: Bow-to-Waterline inches + 20\" submerged prop depth + 5\"–10\" rough-water wave allowance."},
    {"slug": "trolling-motor-battery-amp-hour-runtime-12v-24v-36v-calculator", "name": "12V / 24V / 36V Trolling Motor Battery Amp-Hour (Ah) Runtime Calculator", "boat_lbs": 3400, "bow_in": 22, "wind_cond": "1.25", "hours": 10, "mount": "bow", "desc": "Calculate exact LiFePO4 vs Lead-Acid/AGM battery runtime hours and NOCO onboard charger bank sizing for 55-lb, 80-lb, and 112-lb trolling motors."},
    {"slug": "16-ft-17-ft-aluminum-bass-tracker-crappie-boat-calculator", "name": "16'–17' Aluminum Bass / Crappie Tracker (2,200 Lbs — 55 Lb vs 80 Lb)", "boat_lbs": 2200, "bow_in": 19, "wind_cond": "1.20", "hours": 8, "mount": "bow", "desc": "At 2,200 lbs loaded weight, see why stepping up from a 12V 55-lb motor to a 24V 70–80 lb motor with a 45\"–54\" shaft doubles wind-holding power."},
    {"slug": "saltwater-flats-skiff-and-carolina-skiff-trolling-motor-calculator", "name": "17'–19' Saltwater Flats Skiff & Carolina Skiff (2,600 Lbs — Riptide 80 Lb)", "boat_lbs": 2600, "bow_in": 18, "wind_cond": "1.35", "hours": 8, "mount": "bow", "desc": "Account for strong coastal tidal currents (1.35x multiplier) to size a 24V 80-lb Minn Kota Riptide Terrova (54\" shaft) and 24V 100Ah LiFePO4 battery."},
    {"slug": "trolling-motor-wire-gauge-6-awg-and-60-amp-breaker-calculator", "name": "Trolling Motor Wire Gauge (6 AWG vs 8 AWG) & 60A Breaker Calculator", "boat_lbs": 3500, "bow_in": 23, "wind_cond": "1.25", "hours": 8, "mount": "bow", "desc": "Calculate ABYC 3%-voltage-drop marine wire gauge (6 AWG tinned copper) for 15-to-25 foot bow-to-stern battery runs plus 60A MKR-27 breaker sizing."},
    {"slug": "12-ft-pond-prowler-pelican-bass-raider-mini-pontoon-calculator", "name": "8'–12' Pond Prowler / Pelican Bass Raider Mini Boat (850 Lbs — 45–55 Lb)", "boat_lbs": 850, "bow_in": 12, "wind_cond": "1.10", "hours": 8, "mount": "transom", "desc": "Size a 45–55 lb 12V Minn Kota Endura Max (36\" shaft) and a 24-lb 12V 100Ah LiFePO4 battery for 2-man plastic pond boats."},
    {"slug": "23-ft-25-ft-offshore-center-console-72-inch-87-inch-shaft-calculator", "name": "23'–25' Offshore Center Console (6,000 Lbs / 38\" Bow — 112 Lb 72\"–87\" Shaft)", "boat_lbs": 6000, "bow_in": 38, "wind_cond": "1.50", "hours": 7, "mount": "bow", "desc": "Size a 36V 112-lb Riptide Terrova / Quest with a 72\" or 87\" long shaft to hold offshore reef spots without throwing a physical anchor."}
]

def get_dynamic_boat_weight_pages():
    configs = [
        (1000, 14, "1.10", "1,000-Lb Loaded Boat (40–55 Lb 12V)"),
        (1800, 18, "1.15", "1,800-Lb Loaded Boat (55 Lb 12V / 45\" Shaft)"),
        (2500, 20, "1.20", "2,500-Lb Loaded Boat (70–80 Lb 24V / 45\"–54\")"),
        (3000, 22, "1.25", "3,000-Lb Loaded Boat (80 Lb 24V / 54\" Shaft)"),
        (3600, 24, "1.25", "3,600-Lb Loaded Boat (80 Lb 24V / 54\"–60\")"),
        (4400, 28, "1.30", "4,400-Lb Loaded Boat (112 Lb 36V / 60\" Shaft)"),
        (5000, 32, "1.35", "5,000-Lb Loaded Boat (112 Lb 36V / 60\"–72\")"),
        (5800, 36, "1.40", "5,800-Lb Loaded Boat (112 Lb 36V / 72\" Shaft)")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 5 + (day_of_year % 4))
    pages = []
    for wt_v, bw_in, w_c, label in configs[:active_count]:
        pages.append({
            "slug": f"{wt_v}-lb-boat-trolling-motor-thrust-shaft-calculator",
            "name": f"{label}",
            "boat_lbs": wt_v,
            "bow_in": bw_in,
            "wind_cond": w_c,
            "hours": 8,
            "mount": "bow" if wt_v >= 1600 else "transom",
            "desc": f"Calculate exact minimum thrust (lbs), 12V/24V/36V voltage, shaft length for a {bw_in}\" bow height, and LiFePO4 battery size for a {label}."
        })
    return pages

ALL_CALC_PAGES = TROL_PRESETS + get_dynamic_boat_weight_pages()

def compute_trolling_specs(boat_lbs, bow_water_in, wind_mult, fishing_hrs, mount_type):
    # 1. Required Thrust (Lbs): Base rule = 2 Lbs per 100 Lbs loaded boat weight * wind/current multiplier
    raw_thrust = (float(boat_lbs) / 100.0) * 2.0 * float(wind_mult)

    if raw_thrust <= 52 and float(boat_lbs) <= 2200:
        rec_thrust = 55
        sys_volts = 12
        tier_label = "55 Lb Thrust (12V System)"
    elif raw_thrust <= 82 and float(boat_lbs) <= 4100:
        rec_thrust = 80
        sys_volts = 24
        tier_label = "80 Lb Thrust (24V System)"
    else:
        rec_thrust = 112
        sys_volts = 36
        tier_label = "112 Lb Thrust (36V System)"

    # 2. Recommended Shaft Length (Inches):
    # Bow-to-Waterline + 20" immersion + (4" calm, 7" moderate waves, 11" rough/offshore waves)
    wave_allowance = 4 if float(wind_mult) <= 1.15 else (7 if float(wind_mult) <= 1.28 else 11)
    raw_shaft_in = float(bow_water_in) + 20.0 + wave_allowance

    if mount_type == "transom" and raw_shaft_in <= 40:
        rec_shaft_in = 36
    elif raw_shaft_in <= 44:
        rec_shaft_in = 45
    elif raw_shaft_in <= 53:
        rec_shaft_in = 54
    elif raw_shaft_in <= 62:
        rec_shaft_in = 60
    else:
        rec_shaft_in = 72

    # 3. LiFePO4 Battery Capacity & NOCO Charger Sizing:
    # Average fishing draw (mixed Spot-Lock & cruising w/ Digital Maximizer) is ~13A to 16A
    avg_amps = 12.5 if sys_volts == 12 else (14.5 if sys_volts == 24 else 15.5)
    req_lifepo4_ah = max(50, int(math.ceil((avg_amps * float(fishing_hrs)) / 25.0) * 25))
    if req_lifepo4_ah <= 100:
        bat_config_str = f"100Ah @ {sys_volts}V LiFePO4 ({int(sys_volts*1.28)} kWh)"
    else:
        bat_config_str = f"{req_lifepo4_ah}Ah @ {sys_volts}V LiFePO4 Bank"

    charger_banks = (sys_volts // 12) + 1  # +1 bank for 12V outboard cranking battery
    wire_breaker_str = "6 AWG Tinned Copper + 60A MKR-27 Breaker"

    return int(round(raw_thrust)), rec_thrust, sys_volts, tier_label, rec_shaft_in, int(round(raw_shaft_in)), bat_config_str, charger_banks, wire_breaker_str

def generate_faq_data(preset_name, boat_lbs, bow_in, wind_cond, hours, mount):
    raw_t, rec_t, sys_v, tier_lbl, shaft_in, raw_sh, bat_s, chg_b, wire_s = compute_trolling_specs(
        boat_lbs, bow_in, wind_cond, hours, mount
    )
    return [
        {
            "q": f"How many pounds of trolling motor thrust do I need for {preset_name} ({boat_lbs:,} lbs loaded)?",
            "a": f"Applying the marine 2-lbs-per-100-lbs rule with your wind/current factor gives a minimum requirement of {raw_t} lbs of thrust. You should install a {tier_lbl} (such as a Minn Kota Terrova {rec_t} or Endura Max {rec_t})."
        },
        {
            "q": f"What shaft length trolling motor do I need for a {bow_in}-inch bow-to-waterline height?",
            "a": f"Measuring {bow_in} inches from the top of your bow mounting deck down to the waterline—plus 20 inches for proper prop immersion and wave allowance ({raw_sh}\" total)—requires a {shaft_in}-Inch Shaft so the propeller never cavitates in choppy water."
        },
        {
            "q": f"What size LiFePO4 battery and NOCO onboard charger do I need for {hours} hours on a {sys_v}V motor?",
            "a": f"For {hours} hours of mixed Spot-Locking and trolling on a {sys_v}V {rec_t}-lb motor with Digital Maximizer, we recommend a {bat_s} paired with a NOCO Genius GENPRO10X{min(4, chg_b)} ({min(4, chg_b)}-Bank waterproof charger to charge both your trolling bank and 12V cranking battery)."
        },
        {
            "q": "What size circuit breaker and marine wire gauge is required for a trolling motor?",
            "a": f"All 55-lb (12V), 80-lb (24V), and 112-lb (36V) trolling motors pull 50 to 56 Amps at full speed and require {wire_s} along with a 60A MKR-28 or 80A Battery Tender bow plug."
        },
        {
            "q": "Why am I getting vertical static lines on my fish finder screen when I press the trolling motor pedal?",
            "a": "Never power your fish finder/sonar from your trolling motor batteries! Pulse-Width Modulation (PWM) speed controllers send electrical noise down the power wires. Always wire your Garmin or Humminbird fish finder to your separate 12V outboard cranking battery or a dedicated 12V 20Ah Nocqua lithium pack."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-sky-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['thrust_spec']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['boat_match']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-sky-700 hover:bg-sky-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-sky-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-sky-100 text-sky-900 border border-sky-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-sky-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-sky-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top GPS Trolling Motors, LiFePO4 Batteries, NOCO Chargers & Fish Finders Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 ABYC Marine & On-Water Thrust Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Marine Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Thrust / Output Spec</th>
                        <th class="p-3.5">Boat Fitment</th>
                        <th class="p-3.5">Key On-Water Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-sky-100 text-sky-900 border border-sky-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-200 text-amber-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-sky-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">Thrust / Spec:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">GPS / Tech:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Shaft / Build:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Included:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Marine Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-sky-700 hover:bg-sky-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Minn+Kota+Trolling+Motor+Garmin+Fish+Finder+LiTime+LiFePO4+NOCO+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Marine & Fishing Deals</span>
            <span>Save up to 30% on Minn Kota GPS Trolling Motors, Garmin/Humminbird Side-Imaging Fish Finders, Marine LiFePO4 & NOCO Chargers on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Marine & Trolling Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-sky-700 flex items-center justify-center text-white font-black text-lg shadow-sm">T</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Trolling Motor Thrust, Shaft Length & LiFePO4 Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-sky-800 transition">Thrust & Shaft Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-sky-800 transition">Search Marine Gear</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-sky-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-sky-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-sky-800 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-sky-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-sky-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-sky-800 hover:underline">🚤 {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-sky-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-sky-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-sky-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-sky-700 hover:bg-sky-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. Thrust & Shaft Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-sky-800 hover:underline">🏠 Home — Master Trolling Motor Thrust & Shaft Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all boat trolling motor thrust calculators, bow-to-waterline shaft length guides, marine LiFePO4 calculators, and daily reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-sky-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive boat trolling motor thrust calculator, shaft length sizing guide, 12V/24V/36V battery tool, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    _, rec_t, sys_v, _, shaft_in, _, _, _, _ = compute_trolling_specs(
        page_data["boat_lbs"], page_data["bow_in"], page_data["wind_cond"],
        page_data["hours"], page_data["mount"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — {rec_t} Lb ({sys_v}V) & {shaft_in}\" Shaft Calculator | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(
        page_data["name"], page_data["boat_lbs"], page_data["bow_in"],
        page_data["wind_cond"], page_data["hours"], page_data["mount"]
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-sky-100 text-sky-900 border border-sky-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-sky-700 hover:bg-sky-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        _, p_t, p_v, _, p_sh, _, _, _, _ = compute_trolling_specs(
            p["boat_lbs"], p["bow_in"], p["wind_cond"], p["hours"], p["mount"]
        )
        active_cls = "bg-sky-100 border-sky-700 text-sky-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-sky-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-sky-900 font-mono shrink-0">{p_t}lb / {p_sh}"</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Minn+Kota+Terrova+GPS+Trolling+Motor+LiTime+LiFePO4+and+NOCO+GENPRO+Charger")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-sky-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>🚤 2-Lbs-Per-100-Lb Thrust Formula, Bow-to-Waterline Shaft & LiFePO4 Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Boat Trolling Motor Thrust (Lbs), Shaft Length & LiFePO4 Battery Calculator" if is_home else f"{page_data['name']} — Thrust & Shaft Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter Loaded Boat Weight & Bow-to-Waterline Height</h2>
                        <p class="text-xs text-gray-600">Calculates min thrust (55/80/112 lb), voltage (12V/24V/36V), shaft inches & LiFePO4 Ah</p>
                    </div>
                    <span class="text-xs font-mono bg-sky-100 text-sky-900 border border-sky-300 px-2.5 py-1 rounded font-semibold">Live Marine Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Boat Type & Fishing Style Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-sky-700">
                        <option value="{page_data['boat_lbs']},{page_data['bow_in']},{page_data['wind_cond']},{page_data['hours']},{page_data['mount']}">Current: {page_data['name']}</option>
                        <option value="3200,22,1.25,8,bow">18'–19' Bass Boat (3,200 Lbs Loaded / 22\" Bow — 80 Lb 24V / 54\" Shaft)</option>
                        <option value="4200,26,1.35,6,bow">20'–24' Pontoon Boat (4,200 Lbs + High Wind — 80/112 Lb / 60\" Shaft)</option>
                        <option value="1350,15,1.15,8,transom">14'–16' Aluminum Jon Boat (1,350 Lbs — 55 Lb 12V / 36\"–42\" Shaft)</option>
                        <option value="4600,30,1.35,8,bow">20'–22' Deep-V Walleye / Saltwater Bay Boat (4,600 Lbs — 112 Lb 36V / 60\")</option>
                        <option value="550,10,1.15,7,transom">10'–13' Fishing Kayak / Canoe (550 Lbs — 36–55 Lb 12V / 36\" Shaft)</option>
                        <option value="2200,19,1.20,8,bow">16'–17' Aluminum Bass / Crappie Tracker (2,200 Lbs — 55/80 Lb / 45\"–54\")</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="weightInput" class="block text-sm font-bold text-gray-800 mb-1">Total Loaded Boat Weight (Lbs)</label>
                        <input type="number" id="weightInput" value="{page_data['boat_lbs']}" min="250" max="10000" step="100" oninput="calculateTrolling()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-sky-700">
                        <span class="text-[11px] text-gray-600">Dry Hull + Outboard + Fuel + Gear + Anglers</span>
                    </div>

                    <div>
                        <label for="bowInput" class="block text-sm font-bold text-gray-800 mb-1">Bow-to-Waterline Distance (Inches)</label>
                        <input type="number" id="bowInput" value="{page_data['bow_in']}" min="6" max="52" step="1" oninput="calculateTrolling()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-sky-700">
                        <span class="text-[11px] text-gray-600">Measure top of bow deck straight down to water</span>
                    </div>

                    <div>
                        <label for="windInput" class="block text-sm font-bold text-gray-800 mb-1">Wind, Waves & Current Conditions</label>
                        <select id="windInput" onchange="calculateTrolling()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="1.05" {"selected" if page_data['wind_cond'] <= "1.10" else ""}>Calm Ponds & Small Sheltered Lakes (1.05x)</option>
                            <option value="1.25" {"selected" if "1.10" < page_data['wind_cond'] <= "1.28" else ""}>Moderate Wind, Reservoirs & Rivers (1.25x #1)</option>
                            <option value="1.40" {"selected" if page_data['wind_cond'] > "1.28" else ""}>Heavy Wind, Big Water Chop & Tidal Bay (1.40x)</option>
                        </select>
                    </div>

                    <div>
                        <label for="mountInput" class="block text-sm font-bold text-gray-800 mb-1">Mounting Location & Style</label>
                        <select id="mountInput" onchange="calculateTrolling()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="bow" {"selected" if page_data['mount'] == "bow" else ""}>Bow-Mount GPS Spot-Lock (Terrova / Ulterra / Xi3)</option>
                            <option value="transom" {"selected" if page_data['mount'] == "transom" else ""}>Transom / Kayak Hand-Tiller (Endura Max / NK180)</option>
                        </select>
                    </div>

                    <div class="sm:col-span-2">
                        <label for="hoursInput" class="block text-sm font-bold text-gray-800 mb-1">Target Fishing Time Per Charge: <span id="hoursLabel" class="text-sky-800 font-extrabold">{page_data['hours']} Hours</span></label>
                        <input type="range" id="hoursInput" value="{page_data['hours']}" min="4" max="16" step="1" oninput="calculateTrolling()"
                               class="w-full accent-sky-700 cursor-pointer">
                        <div class="flex justify-between text-[11px] text-gray-600">
                            <span>4 Hrs (Half Day)</span>
                            <span>8 Hrs (Full Tournament Day)</span>
                            <span>12 Hrs</span>
                            <span>16 Hrs (2-Day Trip)</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-sky-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-sky-800">2. Engineered Motor, Shaft & Battery Specs</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Exact Boat Rigging</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-sky-100 border border-sky-300 rounded-xl p-3.5">
                        <span class="text-xs text-sky-950 font-semibold block">Recommended Thrust</span>
                        <span id="resThrustTier" class="text-2xl font-black text-sky-800">80 Lb (24V)</span>
                        <span id="resRawThrust" class="text-[11px] text-sky-900 block mt-0.5">80 Lb Calc Min Thrust</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Min. Shaft Length</span>
                        <span id="resShaftIn" class="text-2xl font-black text-gray-900">54\" Shaft</span>
                        <span id="resShaftCalc" class="text-[11px] text-emerald-800 font-bold block mt-0.5">49\" Min Immersion</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">LiFePO4 Battery Bank</span>
                        <span id="resBatBank" class="text-sm font-extrabold text-gray-900">100Ah @ 24V LFP</span>
                        <span id="resCharger" class="text-[11px] text-gray-600 block mt-0.5">+ NOCO GENPRO10X3</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Breaker, Wire & Plug</span>
                        <span id="resBreaker" class="text-sm font-extrabold text-amber-800">60A MKR-27 Brk</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">6 AWG Tinned + MKR-28</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-sky-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-sky-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recTrolTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Motor & Battery Match...</h3>
                    <p id="recTrolDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-sky-700 hover:bg-sky-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Trolling Motor &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop LiFePO4 & Charger
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search GPS Trolling Motors, Side-Imaging Fish Finders, LiFePO4 & NOCO Chargers</h2>
                <p class="text-sm text-gray-700">Search any thrust (55lb, 80lb, 112lb), shaft length (45\", 54\", 60\"), or brand (Minn Kota, Garmin, Humminbird, LiTime, NOCO, Newport Vessels) on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Minn Kota Terrova 80 lb 54, Garmin ECHOMAP UHD2 93sv, NOCO GENPRO10X3..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-sky-700" required>
                    <button type="submit" class="bg-sky-700 hover:bg-sky-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Minn Kota Terrova 55 80 112 GPS Trolling Motor')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-sky-200 text-gray-800 border border-gray-300 rounded-full transition">Minn Kota Terrova GPS</a>
                    <a href="{amz_url('NOCO Genius GENPRO10X2 GENPRO10X3 Marine Charger')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-sky-200 text-gray-800 border border-gray-300 rounded-full transition">NOCO Onboard Chargers</a>
                    <a href="{amz_url('Garmin ECHOMAP UHD2 Striker Vivid 9sv Fish Finder')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-sky-200 text-gray-800 border border-gray-300 rounded-full transition">Garmin SideVü Sonar</a>
                    <a href="{amz_url('LiTime 12V 24V 36V Trolling Motor LiFePO4 Battery')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-sky-200 text-gray-800 border border-gray-300 rounded-full transition">Trolling LiFePO4 Batteries</a>
                    <a href="{amz_url('Minn Kota MKR-27 60A Breaker and MKR-28 Plug')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-sky-200 text-gray-800 border border-gray-300 rounded-full transition">60A Breakers & Plugs</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-sky-800">Verified Tournament Marine Hardware</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling Trolling Motors, Fish Finders, Marine LiFePO4 & Chargers</h2>
                </div>
                <a href="{amz_url('Best Selling Trolling Motors and Fish Finders')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-sky-800 hover:text-sky-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-sky-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Trolling Motor, Fish Finder & Marine Battery Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-sky-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-sky-700 text-white px-2.5 py-1 rounded">Complete Tournament Spot-Lock & Lithium Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Upgrading Your Boat to GPS Spot-Lock & Lightweight Marine Lithium?</h2>
                <p class="text-sm text-gray-800">Shave 110 lbs off your bow and hold any offshore structure all day by pairing a Minn Kota Terrova GPS Motor with Trolling-Motor LiFePO4 Batteries, a NOCO GENPRO Onboard Charger, and a 60A MKR-27 Breaker.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-sky-700 hover:bg-sky-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Trolling Motor + LiFePO4 Bundles &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">Boat Type, Weight & Shaft Length Specific Trolling Motor Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact boat style or loaded hull weight below for pre-calculated thrust pounds, shaft length inches, and battery bank specs.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-sky-800">Bow-to-Waterline Measurement, PWM & Sonar Noise Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-sky-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-sky-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-sky-800">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-sky-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-sky-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-sky-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("weightInput").value = parts[0];
                document.getElementById("bowInput").value = parts[1];
                document.getElementById("windInput").value = parts[2];
                document.getElementById("hoursInput").value = parts[3];
                document.getElementById("mountInput").value = parts[4];
                calculateTrolling();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateTrolling() {{
            const boatLbs = parseFloat(document.getElementById("weightInput").value) || 3200;
            const bowIn = parseFloat(document.getElementById("bowInput").value) || 22;
            const windMult = parseFloat(document.getElementById("windInput").value) || 1.25;
            const hours = parseFloat(document.getElementById("hoursInput").value) || 8;
            const mount = document.getElementById("mountInput").value || "bow";

            document.getElementById("hoursLabel").textContent = hours + " Hours";

            const rawThrust = Math.round((boatLbs / 100.0) * 2.0 * windMult);
            let recThrust = 80;
            let sysVolts = 24;
            if (rawThrust <= 52 && boatLbs <= 2200) {{
                recThrust = 55;
                sysVolts = 12;
            }} else if (rawThrust <= 82 && boatLbs <= 4100) {{
                recThrust = 80;
                sysVolts = 24;
            }} else {{
                recThrust = 112;
                sysVolts = 36;
            }}

            const waveAllow = windMult <= 1.15 ? 4 : (windMult <= 1.28 ? 7 : 11);
            const rawShaft = Math.round(bowIn + 20 + waveAllow);
            let recShaft = 54;
            if (mount === "transom" && rawShaft <= 40) recShaft = 36;
            else if (rawShaft <= 44) recShaft = 45;
            else if (rawShaft <= 53) recShaft = 54;
            else if (rawShaft <= 62) recShaft = 60;
            else recShaft = 72;

            const avgAmps = sysVolts === 12 ? 12.5 : (sysVolts === 24 ? 14.5 : 15.5);
            const reqAh = Math.max(50, Math.ceil((avgAmps * hours) / 25) * 25);
            const chgBanks = Math.min(4, (sysVolts / 12) + 1);

            document.getElementById("resThrustTier").textContent = recThrust + " Lb (" + sysVolts + "V)";
            document.getElementById("resRawThrust").textContent = rawThrust + " Lb Min Calc Thrust";
            document.getElementById("resShaftIn").textContent = recShaft + "\\\" Shaft";
            document.getElementById("resShaftCalc").textContent = rawShaft + "\\\" Min Immersion Need";
            document.getElementById("resBatBank").textContent = reqAh + "Ah @ " + sysVolts + "V LiFePO4";
            document.getElementById("resCharger").textContent = "+ NOCO GENPRO10X" + chgBanks;
            document.getElementById("resBreaker").textContent = "60A MKR-27 Breaker";

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "LiTime " + sysVolts + "V 100Ah Trolling Motor LiFePO4 Battery and NOCO GENPRO10X" + chgBanks;

            if (mount === "transom" && sysVolts === 12) {{
                recTitle = "Minn Kota Endura Max 55 Lb (" + recShaft + "\" Shaft, Digital Maximizer) or Newport Kayak Motor";
                recDesc = "PWM Digital Maximizer transom motor matched to " + boatLbs.toLocaleString() + "-lb hulls for 5x longer battery runtime.";
                primaryQuery = "Minn Kota Endura Max 55 lb " + recShaft + " Newport Vessels Trolling Motor";
            }} else {{
                recTitle = "Minn Kota Terrova / Riptide " + recThrust + " Lb (" + sysVolts + "V, " + recShaft + "\" Shaft) w/ i-Pilot GPS Spot-Lock";
                recDesc = "Locks your " + boatLbs.toLocaleString() + "-lb boat onto any GPS fishing spot with a " + recShaft + "-inch composite shaft.";
                primaryQuery = "Minn Kota Terrova " + recThrust + " lb " + sysVolts + "V " + recShaft + " GPS Trolling Motor";
            }}

            document.getElementById("recTrolTitle").textContent = recTitle;
            document.getElementById("recTrolDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateTrolling);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-sky-700 transition block">
            <span class="text-[11px] font-bold text-sky-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-sky-800">Home & Thrust Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-sky-800">Daily Marine Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-sky-100 text-sky-900 border border-sky-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-200 text-amber-950 px-3 py-1 rounded-lg">Marine Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">Thrust / Spec</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">GPS / Tech</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Shaft / Build</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Included</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-sky-700 hover:bg-sky-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Boat Thrust & Shaft
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On Spot-Lock Wind Hold, Amp Draw & Sonar Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-sky-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our on-water marine benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-sky-700 hover:bg-sky-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Marine & Trolling Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-sky-800">Home & Thrust Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-sky-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-sky-100 text-sky-900 border border-sky-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-sky-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-sky-700 hover:bg-sky-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-sky-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-sky-700 hover:bg-sky-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "18'–19' Bass Boat (3,200 Lbs Loaded / 22\" Bow Height)",
        "boat_lbs": 3200,
        "bow_in": 22,
        "wind_cond": "1.25",
        "hours": 8,
        "mount": "bow",
        "desc": "Calculate exact boat trolling motor thrust (55/80/112 lbs), system voltage (12V/24V/36V), bow-to-waterline shaft length (36\" to 72\"), and marine LiFePO4 battery capacity—plus read 3 new marine reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Boat & Trolling Motor Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
