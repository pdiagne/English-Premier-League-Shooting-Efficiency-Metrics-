# English-Premier-League-Shooting-Efficiency-Metrics-
Analysis of Premier League player shooting efficiency using SEN (Shot Efficiency Number) and CPG (Conversion Pressure Gradient) metrics. Includes pitch visualizations, player comparisons, and tactical insights.

# Analysis of Premier League Player Shooting Metrics

Metric Descriptions
Shot Efficiency Number (SEN)
SEN measures how efficient a shot is compared to the player's own average performance. The formula combines shot quality (xG), shot outcome (via a result coefficient), and relative performance. Goals receive full credit (1.0), saved shots partial credit (0.6), blocked shots minimal credit (0.2), and missed shots zero (0.0). SEN > 1 means above average efficiency, SEN < 1 means below average.
Conversion Pressure Gradient (CPG)
CPG measures how shot efficiency changes with distance from goal. It shows whether a player maintains their finishing quality from farther away. Positive CPG means efficiency increases with distance (rare), negative CPG means efficiency decreases with distance (expected). Higher CPG indicates a player who is dangerous from more positions on the pitch.
Combined Use: SEN tells you how well a player finishes, while CPG tells you where they are most dangerous. Together, they identify player archetypes—clinical poachers (high SEN, low CPG), long-range threats (moderate SEN, high CPG), or elite all-around finishers (high SEN, high CPG).

Executive Summary
This analysis evaluates 42 Premier League players with at least 350 shots. The Understat data is from the 2014 to 2023 seasons. The data reveals clear distinctions in finishing quality and shooting range among the league's most prolific attackers.

1. Top Performers
Best Finishers (Highest Avg SEN)
Rank	Player	Shots	Avg SEN	Total xG
1	Jamie Vardy	619	0.642	129.8
2	Eden Hazard	355	0.635	46.1
3	Harry Kane	1154	0.628	181.9

Insight: Vardy is the most efficient finisher despite fewer shots than Kane. Kane's volume (1,154 shots) is impressive, but Vardy converts more efficiently.
Best Long-Range Threats (Highest Avg CPG)
Rank	Player	Shots	Avg CPG
1	Roberto Firmino	572	3.2
2	Michail Antonio	513	2.782
3	Raheem Sterling	684	2.723

Insight: Firmino's exceptionally high CPG means he maintains efficiency from distance far better than most strikers—a versatile threat.
Best Goal Conversion Rate
Rank	Player	Shots	Goals	Conversion %
1	Jamie Vardy	619	137	22.13%
2	Callum Wilson	412	88	21.35%
3	Chris Wood	350	70	20.0%

Insight: Vardy dominates both Avg SEN and conversion rate—clearly the Premier League's most efficient finisher among high-volume shooters.

2. Player Archetypes
Archetype	Players	Characteristics
Elite All-Around (High SEN + High CPG)	Firmino, Sterling, Kane	Finish efficiently AND pose threat from distance
Clinical Poachers (High SEN + Low CPG)	Vardy, Hazard, Wilson	Elite finishers but lose efficiency at distance
Long-Range Specialists (Moderate SEN + High CPG)	Antonio, Mané	Maintain efficiency from distance
Inefficient Shooters (Low SEN + Low CPG)	Eriksen, Willian, Coutinho	Need improvement in finishing or shot selection


3. Key Findings
Volume vs. Efficiency
    • Harry Kane (1,154 shots, SEN=0.628): High volume with above-average efficiency
    • James Maddison (446 shots, SEN=0.259): High volume but very low efficiency—poor shot selection
    • Chris Wood (350 shots, SEN=0.569): Lower volume but solid efficiency
CPG Extremes
    • Highest CPG: Firmino (3.2), Antonio (2.782), Sterling (2.723)
    • Lowest CPG: Bruno Fernandes (-0.618), Eriksen (-0.228)
Bruno Fernandes' negative CPG means his efficiency drops sharply with distance—he should shoot closer to goal.
Surprising Insights
    • Son Heung-Min (SEN=0.602, CPG=0.93): Top-10 finisher, consistent across metrics
    • Christian Benteke (SEN=0.487, CPG=0.996): Poor efficiency despite decent range—finishing quality is the issue
    • Olivier Giroud (SEN=0.488, CPG=1.293): Average efficiency but above-average range—useful target man

4. Tactical Implications
Stakeholder	Recommendation
Managers	Deploy Vardy & Kane centrally (high SEN); use Firmino & Sterling in wider roles (high CPG); reduce shots from Maddison & Eriksen (low SEN)
Scouts	Target Vardy-types for counter-attacking systems; target Firmino-types for possession-based systems; avoid high-volume, low-efficiency players like Maddison
Coaches	Train Bruno Fernandes on close-range finishing (negative CPG); encourage Antonio to shoot from distance (high CPG); improve Willian & Coutinho's overall finishing (low SEN)


5. Conclusion
Jamie Vardy is the Premier League's most efficient finisher (highest SEN and conversion rate). Roberto Firmino is the most versatile long-range threat (highest CPG). Elite all-around finishers like Kane, Sterling, and Firmino combine high SEN with strong CPG—making them the most valuable attacking assets.
The data also identifies clear areas for improvement: Maddison and Eriksen take too many low-quality shots, while Bruno Fernandes should focus on closer-range opportunities. These insights enable data-driven decisions on player deployment, scouting, and development.


