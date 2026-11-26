"""Beat sheet, video 3: the bank inside GE. Every figure is from /tmp/ytw/wip/facts.md (row numbers in comments)."""
from engine import INK, RED, GOLD, TEAL, MUTED

GAPS = [0.0, 1.0, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 1.4]
CHAPTERS = {2: (1, "THE SIDE BUSINESS"), 3: (2, "THE ROLLOVER"), 4: (3, "BUFFETT'S PRICE"), 5: (4, "WE NEED HELP"),
            6: (5, "THE BILL"), 7: (6, "THE LEFTOVER"), 8: ("THE REVEAL", "THE REAL LESSON")}
TAIL = 16.0

K = lambda **kw: kw
K10 = "GE Form 10-K, FY2008"
GE8K = "GE Form 8-K, Oct 1, 2008; CNN Money"
PP = "ProPublica, citing Federal Reserve data (Dec 2010)"
PPT = "ProPublica timeline, citing Paulson's memoir 'On the Brink' (2010)"
Q109 = "GE Capital Form 10-Q, Q1 2009"
STOCK = [("Oct 1, 2008", 0.0, 22.25, "$22.25 offer price", "twenty-two dollars and twenty-five cents", TEAL),
         ("Mar 5, 2009", 1.0, 6.66, "$6.66 close", "six dollars and sixty-six cents", RED)]

SECTIONS = [
 # 0 HOOK
 [(None, "factory_bank", K(line1="LIGHT BULBS. JET ENGINES.", line2="…and a bank you never saw.", vault_at="a bank you never saw", l2_at="a bank you never saw")),
  ("On October first", "big_number", K(kicker="OCTOBER 1, 2008", value="$3B", label="special stock sold to Warren Buffett's Berkshire Hathaway", sub="at a 10% dividend", color=GOLD, src=GE8K, when="three billion")),  # 9
  ("Six weeks later", "deal_stack", K(title="GE · AUTUMN 2008", items=[
      ("NOV 12, 2008", "Government guarantee approved for up to", "$139B", "Six weeks later", RED),  # 12
      ("LATE 2008", "Borrowed via a Fed emergency program", "$16B", "It also borrowed", RED),  # 13
      ("MAR 31, 2009", "GE Capital debt guaranteed by the FDIC", "$74B", "By March", RED)],  # 14
      src="GE 8-K; NBC/Reuters; ProPublica (Fed data); GE Capital 10-Q Q1 2009")),
  ("And the stock had fallen", "line_chart", K(title="GE SHARE PRICE", pts=STOCK, lo=0, hi=30, ticks=[0, 10, 20, 30], src="GE offering price (8-K); CNBC")),  # 9, 18
  ("So how does a company", "kinetic", K(lines=[("How does a company", 0.0, {"size": 92, "w": "black"}),
                                                ("that builds jet engines", "that builds jet engines", {"size": 92, "w": "black"}),
                                                ("end up there?", "end up there", {"size": 110, "w": "black", "color": RED})]))],
 # 1 INTRO
 [(None, "title_card", K(title="THE BANK INSIDE GE", sub="GE Capital · 1932–2024", kicker="FOLLOW THE MONEY")),
  ("It made GE one of", "big_number", K(value="~$600B", label="GE's market value, August 2000", color=GOLD, src="Bloomberg; Fortune/CNN Money", when=0.2)),  # 1
  ("We're going to follow", "tl_scene", K(title="THE STORY", items=[("1932", "a small finance office", "from a small finance office", GOLD),
                                                                  ("2008", "the lenders hesitate", "the weeks in two thousand eight", RED)])),
  ("One thing up front", "kinetic", K(lines=[("Legal programs.", 0.0, {"size": 110, "w": "black"}),
                                             ("Open to companies that qualified.", "open to companies", {"size": 64, "color": MUTED}),
                                             ("Not a fraud story.", "This isn't a fraud story", {"size": 90, "w": "black", "color": GOLD}),
                                             ("How money works, and what happens when it stops.", "It's a story about how", {"size": 56})])),
  ("Every number on screen", "kinetic", K(lines=[("Every number: a filing, a regulator", 0.0, {"size": 64, "w": "black"}),
                                                 ("or a named report.", "or a named report", {"size": 64, "w": "black"}),
                                                 ("Sources in the description ↓", "The sources are", {"size": 48, "color": GOLD})]))],
 # 2 THE SIDE BUSINESS
 [(None, "cal_scene", K(top="1932", big="'32", line1="The Great Depression", line2="People want GE's fridges and appliances, but can't pay all at once.")),  # 2
  ("So GE sets up", "factory_bank", K(line1="A small finance arm", line2="Lend customers the money. Get paid back monthly.", vault_at="a small finance arm", l2_at="Lend customers", src="GE Capital history (GE / Business Wire, 2013)")),
  ("In nineteen forty-three", "headline", K(kicker="1943", big="GENERAL ELECTRIC CAPITAL CORPORATION", sub="the finance arm gets its name", color=INK)),
  ("For decades it stays a helper", "bullets", K(title="THEN IT LENDS TO ALMOST ANYONE", items=[("Loans and leases for businesses", "Loans and leases"),
                                                                                               ("Office towers and real estate", "Office towers"),
                                                                                               ("Consumer loans, credit cards, bank accounts", "Consumer loans")],
                                                 src="GE Capital Exit Plan release, Apr 10, 2015 (business lines)")),
  ("It didn't need to sell", "quote", K(s="No GE product needed.", attrib="The bank could make money on its own", size=110)),
  ("By the end of two thousand seven", "hbars", K(title="GE FINANCIAL SERVICES (GECS): TOTAL ASSETS", bars=[
      ("Dec 31, 2007", 646.1, "By the end of two thousand seven", GOLD), ("Jun 30, 2008", 695.8, "By the middle of", RED)],
      prefix="$", unit="B", dec=1, maxv=750, src="GE Form 10-Q and 8-K, 2008")),  # 5
  ("And it earns twelve point four", "profit_split", K(title="2007 EARNINGS", total=22.2, part=12.4, total_lab="All of GE", part_lab="Financial services (GECS)",
      total_at="GE as a whole", part_at="twelve point four", pct_lab="MORE THAN HALF", pct_at="So more than half", src=K10 + " (GECS continuing ops $12,417M; GE $22,208M)")),  # 3
  ("On paper, it was beautiful", "kinetic", K(lines=[("Factories → brand + credit rating", 0.0, {"size": 76, "w": "black"}),
                                                     ("Bank → credit rating into profit", "The bank turned", {"size": 76, "w": "black", "color": GOLD})])),
  ("Wall Street loved it", "big_number", K(value="~$600B", label="GE's market value, August 2000", color=TEAL, src="Bloomberg; Fortune/CNN Money", when="about six hundred")),  # 1
  ("But how does a finance arm", "kinetic", K(lines=[("Not what it lent.", "The secret was not", {"size": 110, "w": "black", "color": MUTED}),
                                                     ("How it borrowed.", "It was how it borrowed", {"size": 120, "w": "black", "color": RED})]))],
 # 3 THE ROLLOVER
 [(None, "headline", K(kicker="GE'S CREDIT RATING", big="AAA", sub="the top grade: GE Capital could borrow more cheaply than almost anyone", color=GOLD, src="S&P (rating held until Mar 12, 2009)")),  # 19
  ("And much of that borrowing", "rollover", K(label="When an IOU comes due, sell a new one")),
  ("As long as investors keep buying", "short_long", K(long_at="lent out as long loans")),
  ("Here's the catch", "kinetic", K(lines=[("A long loan can't be called back early.", 0.0, {"size": 70, "w": "black"}),
                                          ("A short IOU must be repaid on its date.", "A short IOU", {"size": 70, "w": "black", "color": RED}),
                                          ("Find new lenders. Every few weeks.", "So the bank has to", {"size": 70, "w": "black", "color": GOLD})])),
  ("GE became the largest issuer", "big_number", K(kicker="LARGEST US ISSUER OF COMMERCIAL PAPER", value="~$100B", label="outstanding at one point in 2008", color=RED, src=PP, when="almost a hundred billion")),  # 6
  ("That is a lot of money", "rollover", K(label="…borrowed again, every few weeks")),
  ("Now picture September", "cal_scene", K(top="SEP 2008", big="15", line1="Lehman Brothers collapses", line2="Investors ask which big borrower might be next.", color=RED)),
  ("According to the memoir", "filing", K(header="ACCOUNT IN PAULSON'S MEMOIR (AS REPORTED)", title="Calls with GE's CEO", rows=[
      ("Sept 8, 2008", "phone call", "September eighth"), ("Topic", "selling CP", "trouble selling commercial paper"), ("Sept 15, 2008", "spoke again", "spoke again on the fifteenth")],
      caption="Paulson's account", tag=True)),  # 7
  ("GE disputes that account", "compare", K(lt="Paulson's memoir", lv="TROUBLE", rt="GE's letter, Sept 14, 2008", rv="ROBUST", lcol=RED, rcol=TEAL, rat="Its own letter",
      lsub="selling commercial paper", rsub="“commercial paper programs remain robust”", src=PPT, title="TWO ACCOUNTS")),  # 7
  ("But either way", "rollover", K(stop_at="What happens if the lenders stop"))],
 # 4 BUFFETT'S PRICE
 [(None, "cal_scene", K(top="OCT 2008", big="1", line1="GE answers with a show of strength", color=INK)),
  ("Warren Buffett's company", "bond_cert", K(issuer="GENERAL ELECTRIC COMPANY", title="PREFERRED STOCK SOLD TO BERKSHIRE HATHAWAY (SUMMARY)", rows=[
      ("Amount", "$3 billion", "three billion dollars of GE preferred"), ("Dividend", "10% = $300M a year", "It pays a ten percent"),
      ("Buy-back", "after 3 yrs, at 110%", "GE can buy it back"), ("Warrants", "~135M sh @ $22.25", "Buffett also gets warrants")],
      src=GE8K)),  # 9
  ("Those are the terms", "quote", K(s="The terms of a lender who knows he is needed.", size=88, color=INK)),
  ("On the same day", "deal_stack", K(title="FRESH CAPITAL · OCT 2008", items=[
      ("OCT 1", "Berkshire Hathaway preferred stock", "$3B", "On the same day", GOLD),
      ("COMPLETED OCT 7", "547.8M new shares sold at $22.25", "$12.2B", "Within a week", TEAL)],
      total="≈ $15 BILLION IN ONE WEEK", total_at="About fifteen billion", src="GE 8-K; Form 424B2 (547,825,000 shares at $22.25)")),  # 9
  ("And the stock offering means", "kinetic", K(lines=[("More shares →", 0.0, {"size": 100, "w": "black"}),
                                                       ("a smaller slice for every existing owner", "a smaller slice", {"size": 72, "w": "black", "color": RED})])),
  ("For the record", "compare", K(lt="Buffett paid (2008)", lv="$3.0B", rt="GE paid back (2011)", rv="$3.3B", lcol=INK, rcol=GOLD, rat="In two thousand eleven",
      lsub="for the preferred stock", rsub="+ about $900M in dividends along the way", src="Yahoo Finance; GE 8-K terms")),  # 10
  ("But in October two thousand eight", "kinetic", K(lines=[("A company that looked unbreakable…", 0.0, {"size": 76, "w": "black"}),
                                                            ("…sent a signal.", "it was a signal", {"size": 90, "w": "black", "color": GOLD}),
                                                            ("It still wasn't enough.", "And it still wasn't enough", {"size": 100, "w": "black", "color": RED})]))],
 # 5 WE NEED HELP
 [(None, "quote", K(s="“We need help.”", attrib="Immelt to Paulson, October 2008, according to Paulson's memoir", size=150, color=RED)),  # 8
  ("That month, the government", "headline", K(kicker="OCTOBER 2008 · FDIC", big="DEBT GUARANTEE PROGRAM", sub="the FDIC guarantees new bank debt, so lenders keep lending", color=GOLD, src=PPT)),
  ("There was one problem", "compare", K(lt="Traditional bank", lv="YES", rt="GE Capital", rv="NO", lcol=TEAL, rcol=RED, rat="GE Capital wasn't", lsub="eligible", rsub="not a traditional bank: didn't qualify under the first rules", src=PPT, title="WHO QUALIFIED?")),  # 11
  ("A guarantee means this", "kinetic", K(lines=[("If GE Capital can't pay a lender back…", 0.0, {"size": 72, "w": "black"}),
                                                 ("…the FDIC will.", "the FDIC would", {"size": 110, "w": "black", "color": RED})])),
  ("Then the rules changed", "cal_scene", K(top="NOV 2008", big="12", line1="GE Capital approved for the FDIC program", line2="up to $139 billion of debt", color=INK)),  # 12
  ("At the same time", "rollover", K(label="The Fed's program buys the IOUs nobody else will", src="Federal Reserve Commercial Paper Funding Facility")),
  ("Over several weeks", "big_number", K(value="$16B", label="GE's borrowing through the Fed's commercial paper program", sub="over several weeks, late 2008", color=RED, src=PP, when="sixteen billion")),  # 13
  ("It wasn't alone", "big_number", K(value="$738B", label="borrowed by 82 companies through the same program", color=MUTED, src=PP, when="seven hundred")),  # 13
  ("But look at the guarantee", "meter", K(title="GE CAPITAL DEBT GUARANTEED BY THE FDIC", cap=139, cap_lab="approved up to", steps=[
      (35.243, "Dec 31, 2008", "At the end of two thousand eight"), (73.99, "Mar 31, 2009", "Three months later")], src=Q109)),  # 12, 14
  ("GE Capital became the largest user", "headline", K(kicker="FDIC DEBT GUARANTEE PROGRAM", big="LARGEST USER: GE CAPITAL", sub="more than $70B of government-backed debt", color=RED, src=PPT)),  # 15
  ("In December, GE set", "big_number", K(kicker="DECEMBER 2008 · NEW GOAL", value="$50B", label="commercial paper target for 2009", color=GOLD, src="GE outlook, Dec 2008")),  # 16
  ("Under the deal", "kinetic", K(lines=[("GE had to repay the FDIC", 0.0, {"size": 80, "w": "black"}),
                                         ("for anything it paid out.", "for any money it ever paid", {"size": 80, "w": "black"}),
                                         ("But the government's name stood behind it.", "the government's name", {"size": 60, "color": GOLD})], src=Q109))],
 # 6 THE BILL
 [(None, "compare", K(lt="2007", lv="$12.4B", rt="2008", rv="$7.8B", lcol=GOLD, rcol=RED, rat="seven point eight", lsub="financial services earnings", rsub="financial services earnings", src=K10, title="GECS EARNINGS")),  # 3, 4
  ("On February twenty-seventh", "hbars", K(title="GE QUARTERLY DIVIDEND PER SHARE", bars=[("Before", 31, 0.3, TEAL), ("From 2009 (cut announced Feb 27, 2009)", 10, "to ten cents", RED)],
      unit="¢", maxv=35, note="First cut since 1938 · saves about $9B a year", src="AP/NBC News, Feb 27, 2009")),  # 17
  ("On March fifth", "line_chart", K(title="GE SHARE PRICE", pts=STOCK, lo=0, hi=30, ticks=[0, 10, 20, 30], src="GE offering price (8-K); CNBC")),  # 18
  ("A week later", "compare", K(lt="Before", lv="AAA", rt="March 12, 2009", rv="AA+", lcol=GOLD, rcol=RED, rat="took away", lsub="S&P rating", rsub="S&P rating", src="CNN Money, Mar 12, 2009", title="THE CHEAP MONEY ENDS")),  # 19
  ("So GE started to shrink", "hbars", K(title="GECS COMMERCIAL PAPER OUTSTANDING", bars=[("Dec 31, 2008", 71.8, "Commercial paper went", RED), ("Dec 31, 2009", 47.3, "forty-seven point three", TEAL)],
      prefix="$", unit="B", dec=1, maxv=80, src="GE Form 10-K, FY2009")),  # 16
  ("In two thousand thirteen", "headline", K(kicker="2013 · FINANCIAL STABILITY OVERSIGHT COUNCIL", big="SYSTEMICALLY IMPORTANT", sub="concern: reliance on short-term funding", color=RED, src="FSOC; A&O Shearman summary")),  # 20
  ("And in April two thousand fifteen", "big_number", K(kicker="APRIL 10, 2015 · GE CAPITAL EXIT PLAN", value="~$200B", label="of GE Capital to be sold within two years", color=GOLD, src="GE release, Apr 10, 2015 (ending net investment)", when="about two hundred")),  # 21
  ("Real estate went first", "deal_stack", K(title="THE SELL-OFF BEGINS", items=[
      ("2015", "Real estate deals, much of it to Blackstone funds", "$26.5B", "Real estate went first", GOLD),
      ("1Q 2015", "First charge (after tax)", "~$16B", "The first charge", RED)], src="GE release, Apr 10, 2015")),  # 21
  ("In two thousand fourteen", "hbars", K(title="SHARE OF GE EARNINGS FROM INDUSTRIAL BUSINESSES", bars=[("2014", 58, "only fifty-eight", MUTED), ("2018 goal", 90, "more than ninety", TEAL)],
      unit="%", maxv=100, note="Stock rose 11% the day of the announcement", src="GE release, Apr 10, 2015; Fortune")),  # 21
  ("A year later, in June", "headline", K(kicker="JUNE 2016 · UNANIMOUS VOTE", big="LABEL REMOVED", sub="assets cut by more than half · the first time ever", color=TEAL, src="US Treasury / FSOC, June 2016; Davis Polk")),  # 22
  ("It looked like the story", "kinetic", K(lines=[("The story was over.", 0.0, {"size": 110, "w": "black", "color": MUTED}),
                                                   ("It wasn't.", "It wasn't", {"size": 150, "w": "black", "color": RED})]))],
 # 7 THE LEFTOVER
 [(None, "factory_bank", K(line1="What was left of GE Capital…", line2="…an old insurance business", vault_at=0.3, l2_at="an old insurance business")),
  ("It had taken on long-term care", "insurance_clock", K(src="GE release, Jan 16, 2018")),  # 24
  ("In two thousand eighteen, GE found out", "headline", K(kicker="2018", big="OLD ESTIMATES: TOO LOW", sub="the long-term care costs were higher than GE had assumed", color=RED, src="GE release, Jan 16, 2018")),
  ("In January two thousand eighteen", "deal_stack", K(title="JANUARY 16, 2018", items=[
      ("4Q 2017", "Charge after tax", "$6.2B", "A six point two", RED),
      ("2018–2024", "Put into the insurance business over 7 years", "~$15B", "And about fifteen billion", RED),
      ("SCHEDULE", "About $3B right away, then about $2B a year", "", "About three billion", GOLD),
      ("ALSO", "GE Capital dividends to its parent: stopped", "", "And GE Capital would stop", MUTED)], src="GE release, Jan 16, 2018")),  # 24
  ("By then, the dividend", "hbars", K(title="GE QUARTERLY DIVIDEND PER SHARE", bars=[("2008", 31, 0.3, TEAL), ("2009", 10, 0.3, GOLD), ("Nov 2017", 12, "to twelve cents", GOLD), ("Oct 2018", 1, "to one cent", RED)],
      unit="¢", maxv=35, gap=150, y0=260, src="AP/NBC; Fortune")),  # 17, 23, 26
  ("In June two thousand eighteen", "dow_board", K(out_at="removed from the Dow", src="NPR, June 19, 2018")),  # 25
  ("In October, a new chief executive", "big_number", K(kicker="Q3 2018", value="−$22.8B", label="quarterly loss, mostly a power business write-down", sub="dividend cut to 1¢ a share", color=RED, src="Reuters/Business Standard; Fortune, Oct 30, 2018", when=0.2)),  # 26
  ("By January two thousand nineteen", "hbars", K(title="GE MARKET VALUE", bars=[("August 2000 (peak)", 600, "At its peak", GOLD), ("January 2019", 75, "seventy-five billion", RED)],
      prefix="~$", unit="B", maxv=650, src="Bloomberg")),  # 1, 27
  ("In two thousand twenty", "filing", K(header="SEC ORDER (SUMMARY) · DEC 9, 2020", title="Settled: $200 million penalty", rows=[
      ("Power profits", "cost estimates cut", "a large part of its power profits"), ("Insurance costs", "uncertainty", "lowered expected insurance"),
      ("GE", "no admission", "neither admitted nor denied"), ("Restatement", "not required", "did not have to restate")],
      caption="$200M penalty")),  # 28
  ("GE neither admitted", "kinetic", K(lines=[("Neither admitted nor denied.", 0.0, {"size": 90, "w": "black"}),
                                              ("No restatement required.", "did not have to restate", {"size": 80, "w": "black", "color": MUTED})], src="SEC press release 2020-312"))],
 # 8 THE REAL LESSON
 [(None, "kinetic", K(lines=[("So what happened to GE?", 0.0, {"size": 100, "w": "black"})])),
  ("GE broke itself up", "breakup", K(names=[("GE HEALTHCARE", "spun off Jan 2023", "GE HealthCare was spun off"), ("GE VERNOVA", "power · spun off Apr 2024", "GE Vernova, the power"),
                                            ("GE AEROSPACE", "what remained", "What remained")], at="GE broke itself up", src="GE spin-off FAQ")),  # 29
  ("And here is the twist", "turbine", K(counters=[("GE Vernova orders, Q3 2026", 29.3, "$", "B", 1, "twenty-nine point three"), ("total backlog", 197, "$", "B", 0, "a hundred and ninety-seven")],
                                       src="GE Vernova Q3 2026 results (8-K)")),  # 30
  ("Its gas turbine backlog", "hbars", K(title="GE VERNOVA GAS BACKLOG + SLOT RESERVATIONS", bars=[("Q3 2026", 122, "a hundred and twenty-two", GOLD), ("expected by end of 2026", 130, "at least a hundred and thirty", TEAL)],
      unit=" GW", maxv=140, note="CEO: data centers ~1/3 of its US gas power deals", src="GE Vernova Q3 2026 results; CEO remarks as reported")),  # 30, 31
  ("The machines GE built", "factory_bank", K(line1="A century of machines…", line2="…now powering the newest borrowing boom", l2_at="now powering")),
  ("Which brings us back", "short_long", K(long_at="lent it out for years")),
  ("That works every day", "rollover", K(stop_at="until the day lenders hesitate")),
  ("Notice what saved GE", "bullets", K(title="WHAT SAVED GE: OUTSIDE MONEY, ARRIVING FAST", items=[("Buffett's capital: $3B", "Buffett's capital"), ("New shareholders: $12.2B", "new shareholders"),
                                                                                               ("The Fed's program: $16B", "the Fed's program"), ("The FDIC's name: up to $139B", "the FDIC's name")])),
  ("And notice what it cost", "bullets", K(title="WHAT IT COST", items=[("A diluted stock", "A diluted stock"), ("A lost AAA rating", "A lost triple A"),
                                                                       ("A decade of shrinking", "A decade of shrinking"), ("An insurance bill, 10 years later", "And an insurance bill")])),
  ("The bank had made GE look", "kinetic", K(lines=[("Profits: every quarter.", 0.0, {"size": 100, "w": "black", "color": TEAL}),
                                                    ("Risk: only when the funding stopped.", "the risk only showed up", {"size": 80, "w": "black", "color": RED})])),
  ("If you watched our last video", "watch", K(items=[("1", "Who is lending?", "Who is lending"), ("2", "For how long?", "for how long"), ("3", "What happens if they stop?", "what happens if they stop")]))],
 # 9 CLOSE
 [(None, "kinetic", K(lines=[("GE survived.", 0.0, {"size": 110, "w": "black"}),
                             ("Buffett got his dividends.", "Buffett got", {"size": 70, "color": GOLD}),
                             ("The guarantee was there when needed.", "The government's guarantee", {"size": 70, "color": MUTED})])),
  ("But it took fifteen years", "bullets", K(title="WHAT IT TOOK", items=[("~15 years", "fifteen years"), ("A lost credit rating", "a lost credit rating"), ("3 dividend cuts", "three dividend cuts"), ("A breakup", "and a breakup")])),
  ("So here's my question", "compare", K(lt="Genius idea", lv="TOO FAR?", rt="Hidden risk", rv="ALWAYS THERE?", lcol=GOLD, rcol=RED, rat="or a risk", lsub="that went too far", rsub="in plain sight", title="YOUR CALL · TELL ME IN THE COMMENTS")),
  ("Next, we go back", "endscreen", K(next_title="ENRON: WHO ACTUALLY\nLOST THE MONEY"))],
]
