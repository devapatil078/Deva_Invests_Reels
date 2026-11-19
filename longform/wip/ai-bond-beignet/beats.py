"""Beat sheet, video 2: the Beignet bond. Every figure is from /tmp/ytw/wip/facts.md (row numbers in comments)."""
from engine import INK, RED, GOLD, TEAL, MUTED

GAPS = [0.0, 1.0, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 1.4]
CHAPTERS = {2: (1, "THE BUILDING"), 3: (2, "THE PASTRY COMPANY"), 4: (3, "THE RUSH"), 5: (4, "THE QUIET EXIT"),
            6: (5, "THE SLIDE"), 7: (6, "THE BILL"), 8: ("THE REVEAL", "THE MISMATCH")}
TAIL = 16.0

K = lambda **kw: kw
B = "Bloomberg via Advisor Perspectives, Oct 28, 2026"
REL = "Meta release, Oct 21, 2025"
SP = "S&P Global Ratings, Oct 30, 2026 (as reported)"
Q3 = "Meta Form 10-Q, Q3 2026"
PR = [None, "Within days", "Then the biggest lender", "In September", "By October"]

SECTIONS = [
 # 0 HOOK
 [(None, "pastry_name2", K(name="BEIGNET INVESTOR LLC", line2="named after a fried pastry from New Orleans", big="$27.3B", big_at="twenty-seven point three", src="IFR; Meta release, Oct 21, 2025")),  # 6
  ("from the kind of funds", "kinetic", K(lines=[("Borrowed from funds that manage", 0.0, {"size": 56, "color": MUTED}),
                                                  ("PENSIONS + INSURANCE MONEY", "pensions", {"size": 96, "w": "black"})])),
  ("All of it to pay", "la_map", K(caption="ONE BUILDING", sub="Meta's Hyperion AI data center", src=REL)),
  ("Within days", "price_chart", K(upto=2, anchors=[None, "a hundred and ten"], src="Bloomberg; Protos")),  # 9
  ("Then the biggest lender", "sell_blocks", K(src=B)),  # 10
  ("In September", "stock_vs_bond", K(src="Protos, Sep 23, 2026")),  # 13
  ("By October", "price_chart", K(upto=5, anchors=[0, 0, 0, 0, "ninety-two"], src="Bloomberg; Protos; Enterprise, Oct 19, 2026"))],  # 14
 # 1 INTRO
 [(None, "kinetic", K(lines=[("Who lent the money?", 0.0, {"size": 92, "w": "black"}),
                             ("What did Meta promise?", "What did Meta", {"size": 92, "w": "black"}),
                             ("Why is the bond market nervous?", "And why is", {"size": 92, "w": "black", "color": RED})])),
  ("We're going to follow", "title_card", K(title="THE $27 BILLION AI BOND", sub="Meta · Hyperion · Beignet Investor · 2025–2026", kicker="FOLLOW ONE BOND")),
  ("One thing up front", "kinetic", K(lines=[("Legal. Disclosed.", 0.0, {"size": 110, "w": "black"}),
                                             ("No one is accused of wrongdoing.", "no one is accused", {"size": 64, "color": MUTED}),
                                             ("This is how the AI boom is paid for.", "Because this is how", {"size": 64, "color": GOLD})]))],
 # 2 THE BUILDING
 [(None, "la_map", K(caption="RICHLAND PARISH", sub="farmland, north-east Louisiana", src=REL)),
  ("Mark Zuckerberg has said", "quote", K(s="“a significant part of the footprint of Manhattan”", attrib="Mark Zuckerberg on Hyperion, as reported by Fortune", size=80)),  # 18
  ("To power it", "plants", K(src="Entergy; Fortune, Mar 27, 2026")),  # 17
  ("Fortune estimated", "big_number", K(value="~$11B", label="estimated cost of the 10 gas plants", sub="+ 240 miles of new transmission lines, paid for by Meta", color=GOLD, src="Fortune, Mar 27, 2026", when=0.2)),
  ("Getting there was its own fight", "votes", K(rows=[("AUGUST 2025", "First 3 gas plants approved", "4–1", "In August twenty twenty-five"),
                                                       ("APRIL 2026", "Fast-track for 7 more plants", "4–1", "In April twenty twenty-six"),
                                                       ("AUGUST 2026", "Judge's disclosure ruling overturned", "VOTE", "And in August twenty twenty-six")],
                                                 src="LPSC votes as reported by WRKF/WWNO, UCS, E&E News")),  # 19
  ("Critics, like the Union", "kinetic", K(lines=[("Critics: local customers", 0.0, {"size": 76, "w": "black"}),
                                                  ("could be left with part of the bill.", "could be left", {"size": 76, "w": "black", "color": RED})], src="Union of Concerned Scientists")),
  ("And in August twenty twenty-six", "headline", K(kicker="AUGUST 2026", big="NO DISCLOSURE ORDER", sub="Commission overturned a judge's ruling: Meta not forced to disclose projected energy use and jobs", color=GOLD, src="E&E News; WRKF/WWNO")),
  ("The data center itself", "big_number", K(value="~$27B", label="development costs for the Hyperion campus", color=RED, src=REL, kicker="THE DATA CENTER")),  # 1
  ("And Hyperion is only one project", "big_number", K(value="$135–145B", label="Meta's expected 2026 capital spending", sub="Q3 2026 alone: $34.91B", when="between one hundred", src="Meta Q3 2026 results", size=170)),  # 20
  ("Meta can afford a lot", "big_number", K(value="$64.6B", label="Meta revenue, Q3 2026", sub="up 26% from a year earlier", color=TEAL, src="Meta Q3 2026 results")),  # 20
  ("But every giant company", "kinetic", K(lines=[("Borrow $27B for one building…", 0.0, {"size": 76, "w": "black"}),
                                                  ("= $27B of new debt on your balance sheet", "that's twenty-seven", {"size": 60, "color": RED}),
                                                  ("Ratings agencies see it.", "Ratings agencies", {"size": 56, "color": MUTED}),
                                                  ("Bond investors see it.", "Bond investors see it", {"size": 56, "color": MUTED})])),
  ("So Meta did something else", "kinetic", K(lines=[("Someone else borrows.", 0.0, {"size": 110, "w": "black"}),
                                                     ("Someone Meta only partly owns.", "Someone Meta only", {"size": 72, "color": GOLD})]))],
 # 3 THE PASTRY COMPANY
 [(None, "cal_scene", K(top="OCT 2025", big="21", line1="Meta announces a joint venture with Blue Owl Capital funds", line2="a private investment firm")),
  ("The split", "structure", K(stage=1, src=REL)),  # 1
  ("Blue Owl put in", "money_flow", K(src=REL)),  # 2
  ("The rest of the money came from a bond", "bond_cert", K(rows=[("Amount", "$27.3 billion", "twenty-seven point three"),
                                                                 ("Coupon", "6.581% a year", "six point five eight one"),
                                                                 ("Final maturity", "May 30, 2049", "May twenty forty-nine"),
                                                                 ("Rating (S&P)", "A+", "S and P rated it")],
                                                           caption="Almost 24 years", src="IFR; deal summaries citing IFR")),  # 6
  ("S and P rated it A plus", "compare", K(lt="Beignet bond", lv="A+", rt="Meta itself", rv="AA-", lcol=GOLD, rcol=TEAL, rat="Meta's own rating", lsub="S&P rating", rsub="S&P rating", src="IFR; S&P", title="ONE NOTCH APART")),  # 7
  ("So why would lenders", "kinetic", K(lines=[("20% Meta…", 0.0, {"size": 120, "w": "black"}),
                                              ("…rated almost like Meta.", "almost like Meta itself", {"size": 90, "w": "black", "color": GOLD}),
                                              ("Two promises.", "Because of two promises", {"size": 90, "w": "black", "color": RED})])),
  ("Promise one", "structure", K(stage=3, src=REL)),  # 3, 4
  ("It's called a residual value guarantee", "headline", K(kicker="PROMISE TWO", big="RESIDUAL VALUE GUARANTEE", sub="first 16 years of operations · capped cash payment", color=GOLD, src=REL)),
  ("And here's the clever part", "compare", K(lt="The debt", lv="REAL", rt="On Meta's balance sheet?", rv="NO", lcol=INK, rcol=RED, rat="In plain English", lsub="$27.3B of bonds", rsub="a venture Meta does not consolidate", src="Meta 10-Q filings"))],  # 22
 # 4 THE RUSH
 [(None, "structure", K(stage=2, src=B)),  # 8
  ("Bond managers like Pimco", "kinetic", K(lines=[("Whose money?", 0.0, {"size": 70, "color": MUTED}),
                                                   ("PENSION FUNDS", "pension funds", {"size": 100, "w": "black"}),
                                                   ("INSURERS", "insurers", {"size": 100, "w": "black"}),
                                                   ("ORDINARY SAVERS", "ordinary savers", {"size": 100, "w": "black", "color": GOLD})])),
  ("The rest went to other", "headline", K(kicker="HOW IT WAS SOLD", big="PRIVATE OFFERING", sub="only to large institutions", color=INK, src=REL)),  # 5
  ("And the demand was enormous", "price_chart", K(upto=2, anchors=[None, "one hundred and ten"], src=B)),  # 9
  ("Here's what that means", "seesaw", K()),
  ("So a hundred and ten", "big_number", K(value="110", label="cents on the dollar: lenders fighting to get in", color=TEAL, src=B)),
  ("Nine days after", "big_number", K(value="$125B", label="of orders for Meta's own $30B bond sale", sub="a record for a U.S. corporate bond · Oct 30, 2025 · longest bond: 40 years", color=TEAL, src="Bloomberg, Oct 30, 2025", when="a hundred and twenty-five")),  # 15
  ("Everyone believed", "kinetic", K(lines=[("Real AI demand.", 0.0, {"size": 84, "w": "black"}),
                                           ("Growing revenue.", "Meta's revenue was growing", {"size": 84, "w": "black"}),
                                           ("6.581% at A+.", "six and a half percent", {"size": 84, "w": "black", "color": GOLD})])),
  ("Almost everyone", "quote", K(s="One buyer was already doing something else.", size=84, color=RED))],
 # 5 THE QUIET EXIT
 [(None, "sell_blocks", K(src=B)),  # 10
  ("That Oracle deal", "big_number", K(value="$14B", label="of bonds for Oracle's Saline Township, Michigan campus", sub="sold April 2026 · Pimco bought ~$10B", color=GOLD, src="Quartz; The Next Web, Apr 2026")),  # 11
  ("According to Bloomberg, citing trade data", "price_chart", K(upto=2, pts=[("issued", 0.0, 98.7, "98.7"), ("Oct 2026", 1.0, 88.0, "~88")],
                                                                  anchors=[None, "have dropped"], src=B + " (TRACE data)")),  # 12
  ("Pimco hasn't explained", "kinetic", K(lines=[("Pimco declined to comment.", 0.0, {"size": 76, "w": "black"}),
                                                 ("Selling isn't wrongdoing.", "Selling part", {"size": 76, "w": "black", "color": MUTED}),
                                                 ("Big funds rebalance all the time.", "Big funds rebalance", {"size": 60, "color": MUTED}),
                                                 ("Still among the largest holders.", "And Pimco is still", {"size": 60, "color": GOLD})], src=B)),
  ("Bloomberg also reported", "headline", K(kicker="ALSO SKIPPED", big="~$11B", sub="SoftBank's junk bond, among later AI debt deals Pimco passed on", color=GOLD, src=B)),
  ("But look at the timing", "price_chart", K(upto=2, anchors=[None, None], src=B, note="Pimco sold ~$3B while the bonds traded above face value")),
  ("And then the price", "quote", K(s="And then the price started to fall.", size=96, color=RED))],
 # 6 THE SLIDE
 [(None, "price_chart", K(upto=3, anchors=[0, 0, "around ninety-six"], src="Protos, Sep 23, 2026")),  # 13
  ("On September twenty-third", "price_chart", K(upto=4, anchors=[0, 0, 0, "ninety-four point four"], src="Protos, Sep 23, 2026")),
  ("The stock market and the bond market", "stock_vs_bond", K(src="Protos, Sep 23, 2026")),
  ("By mid-October", "price_chart", K(upto=5, anchors=[0, 0, 0, 0, "just under ninety-two"], src="Enterprise, Oct 19, 2026")),  # 14
  ("That's not a default", "compare", K(lt="Bought at", lv="100", rt="Mid-October 2026", rv="~92", lcol=TEAL, rcol=RED, rat="anyone who bought", lsub="face value", rsub="≈ 8 cents lost per dollar, on paper", src="Enterprise, Oct 19, 2026", title="NOT A DEFAULT · META IS PAYING")),
  ("Then came the sequel", "pastry_name2", K(name="SOPAIPILLA INVESTOR", line2="El Paso, Texas · BlackRock-managed entities own 80%", big="~$12.5B", big_at="twelve and a half", src="IBTimes; The Next Web, Jul 2026")),  # 16
  ("Now look at the price", "compare", K(lt="Beignet coupon (2025)", lv="6.581%", rt="Sopaipilla yield (2026)", rv="~7.5%", lcol=GOLD, rcol=RED, rat="It yielded", lsub="Louisiana", rsub="El Paso · due 2048", src="IFR; IBTimes, Jul 2026", title="THE SEQUEL COST MORE")),  # 6, 16
  ("And orders were about", "hbars", K(title="ORDERS FOR THE DEAL", bars=[("Meta's own bonds · Oct 2025", 125, "Compare that", TEAL), ("Sopaipilla · Jul 2026", 20, "And orders were", RED)],
                                       prefix="$", unit="B", src="Bloomberg; IBTimes", note="~1.6x the El Paso deal size")),
  ("Same company", "kinetic", K(lines=[("Same company. Same idea.", 0.0, {"size": 90, "w": "black"}),
                                      ("More interest.", "they wanted more interest", {"size": 90, "w": "black", "color": RED}),
                                      ("Fewer buyers fighting to get in.", "far fewer", {"size": 64, "color": MUTED})]))],
 # 7 THE BILL
 [(None, "headline", K(kicker="WHAT IS META ON THE HOOK FOR?", big="IT'S IN THE FILINGS", color=INK, src=Q3)),
  ("Meta reports something called", "exposure", K(src=Q3 + "; FY2025 10-K")),  # 21
  ("Remember, Meta owns twenty percent", "compare", K(lt="Meta owns", lv="20%", rt="Meta could lose up to", rv="$68.4B", lcol=INK, rcol=RED, rat="Its possible loss", lsub="of the ventures", rsub="maximum exposure to loss, Sep 30, 2026", src=Q3)),
  ("And the ratings agencies noticed", "cal_scene", K(top="OCT 2026", big="30", line1="S&P: Meta outlook cut to NEGATIVE", line2="AA- rating kept", color=RED)),  # 24
  ("But it said Meta's future lease", "hbars", K(title="META, SEPT 30, 2026", bars=[("Future lease obligations", 355.7, "future lease obligations", RED), ("Long-term debt", 80.92, "eighty-one billion", TEAL)],
                                                  prefix="$", unit="B", dec=1, src=SP, note="S&P counts leases like these as debt")),
  ("Its math is simple", "leverage", K(src=SP)),
  ("It expects Meta's free operating", "hbars", K(title="S&P: META FREE OPERATING CASH FLOW DEFICIT (expected)", bars=[("2026", 39, "thirty-nine billion", RED), ("2027", 71, "seventy-one billion", RED)],
                                                  prefix="-$", unit="B", src=SP, note="2028 shortfall expected to be covered entirely with debt")),
  ("S and P also said", "quote", K(s="“Meta's ability to monetize its AI investments is more limited than that of its peers.”", attrib="S&P · Meta: “We respectfully disagree.”", size=64)),
  ("So off the balance sheet", "kinetic", K(lines=[("Off the balance sheet", 0.0, {"size": 96, "w": "black"}),
                                                   ("≠ off the hook.", "never meant off the hook", {"size": 120, "w": "black", "color": RED})]))],
 # 8 THE MISMATCH
 [(None, "headline", K(kicker="THE REAL NUMBER", big="IT'S A DATE", color=RED)),
  ("The Beignet bond runs until", "mismatch", K(src="IFR; Meta release; Meta FY2025 10-K", rows=[
      ("Bond", 23.6, "The Beignet bond runs", RED), ("Lease term", 4, "Meta's lease runs", TEAL), ("Guarantee", 16, "The guarantee covers", GOLD),
      ("Servers", 5.5, "And the computers", (150, 160, 190))])),
  ("Before twenty twenty-five", "compare", K(lt="Server life before 2025", lv="4–5 yrs", rt="Server life from 2025", rv="5.5 yrs", lcol=MUTED, rcol=GOLD, rat="Meta said that one change", lsub="Meta 10-K", rsub="~$2.9B less 2025 depreciation", src="Meta FY2025 10-K; Meta Q4 2024 results")),  # 23
  ("Even so, depreciation", "hbars", K(title="META DEPRECIATION · SERVERS & NETWORK GEAR", bars=[("2023", 7.32, "seven point three two", TEAL), ("2025", 13.36, "thirteen point three six", RED)],
                                        prefix="$", unit="B", dec=2, src="Meta FY2025 10-K")),
  ("So picture the timeline", "mismatch", K(src="IFR; Meta release; Meta FY2025 10-K", rows=[
      ("Bond", 23.6, 0.0, RED), ("Servers", 5.5, "wear out", (150, 160, 190)), ("Lease term", 4, "The tenant can leave", TEAL), ("Guarantee", 16, "And the guarantee", GOLD)])),
  ("That's the mismatch", "kinetic", K(lines=[("A long loan", 0.0, {"size": 120, "w": "black"}),
                                             ("against something that ages fast.", "against something", {"size": 80, "w": "black", "color": RED})])),
  ("And it isn't just Meta", "bar_chart", K(title="AI firms' share of all investment-grade bond issuance", bars=[("2023", 2, "two percent", TEAL), ("2026", 10, "ten percent", RED)], maxv=12,
                                            src="Federal Reserve Bank of Kansas City, Oct 2026")),  # 25
  ("Their bonds run longer", "kinetic", K(lines=[("Longer than the ~10-year market average.", 0.0, {"size": 64, "w": "black"}),
                                                 ("Much of it outside the banking system.", "outside the banking", {"size": 64, "w": "black", "color": GOLD}),
                                                 ("“Lasting consequences” for lenders.", "Its conclusion", {"size": 64, "w": "black", "color": RED})], src="Federal Reserve Bank of Kansas City, Oct 2026")),
  ("Here's the fair version", "compare", K(lt="New Meta bonds · Nov 2026", lv="$15B", rt="Orders", rv="up to $58B", lcol=INK, rcol=TEAL, rat="orders reached", lsub="U.S. dollar sale", rsub="demand is still there", src="Bloomberg, Nov 3, 2026", title="THE FAIR VERSION")),  # 27
  ("Days later, Meta sold", "big_number", K(value="€9B", label="Meta's first euro bonds · longest due 2065", color=TEAL, src="Meta 8-K via PPC Land; Reuters/Bloomberg, Nov 2026")),
  ("But the price has changed", "coupons", K(src="Bloomberg, Oct 30, 2025; Meta notes, Nov 2026"))],  # 15, 27
 # 9 CLOSE
 [(None, "kinetic", K(lines=[("Who is holding it?", 0.0, {"size": 70, "color": MUTED}),
                             ("Pimco, with a smaller stake.", "Pimco, with", {"size": 76, "w": "black"}),
                             ("Other big funds.", "Other big funds", {"size": 76, "w": "black"}),
                             ("Pensions · insurers · savers", "And through them", {"size": 76, "w": "black", "color": GOLD})])),
  ("If you want to follow it", "watch", K(items=[("1", "The Beignet bond price", "The Beignet bond price"),
                                                 ("2", "Meta's maximum exposure to loss, every quarter", "The maximum exposure"),
                                                 ("3", "Louisiana's vote on 7 new gas plants", "And Louisiana")], src="WBRZ: vote expected December 2026")),
  ("None of this means", "risk_moved", K()),
  ("Tell me in the comments", "quote", K(s="Which AI deal should we follow next?", attrib="Tell me in the comments", size=90, color=GOLD)),
  ("watch this next", "endscreen", K())],
]
