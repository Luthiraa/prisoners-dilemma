
WikipediaThe Free Encyclopedia
Search Wikipedia
Search
Donate
Create account
Log in
Contents hide
(Top)
Premise
Strategy for the prisoner's dilemma
Generalized form
The iterated prisoner's dilemma

Real-life examples

Related games

Software
In fiction
In moral philosophy

See also
Notes
References

Further reading
External links
Prisoner's dilemma

Article
Talk
Read
Edit
View history

Tools
Appearance hide
Birthday mode (Baby Globe)

Disabled

Enabled
Learn more about Birthday mode
Text

Small

Standard

Large
Width

Standard

Wide
Color (beta)

Automatic

Light

Dark
From Wikipedia, the free encyclopedia
For other uses, see Prisoner's dilemma (disambiguation).
Not to be confused with Three prisoners problem, Unexpected hanging paradox, 100 prisoners problem, or Innocent prisoner's dilemma.
The prisoner's dilemma is a game theory thought experiment involving two rational agents, each of whom can either cooperate for mutual benefit or betray their partner ("defect") for individual gain. The dilemma arises from the fact that while defecting is rational for each agent, cooperation yields a higher payoff for each. The puzzle was designed by Merrill Flood and Melvin Dresher in 1950 during their work at the RAND Corporation.[1] They invited economist Armen Alchian and mathematician John Williams to play a hundred rounds of the game, observing that Alchian and Williams often chose to cooperate. When asked about the results, John Nash remarked that rational behavior in the iterated version of the game can differ from that in a single-round version. This insight anticipated a key result in game theory: cooperation can emerge in repeated interactions, even in situations where it is not rational in a one-off interaction.

Albert W. Tucker later named the game the "prisoner's dilemma" by framing the rewards in terms of prison sentences.[2] The prisoner's dilemma models many real-world situations involving strategic behavior. In casual usage, the label "prisoner's dilemma" is applied to any situation in which two entities can gain important benefits by cooperating or suffer by failing to do so, but find it difficult or expensive to coordinate their choices.

Premise

An example prisoner's dilemma payoff matrix
This "typical contemporary version" of the game is described in William Poundstone's 1993 book Prisoner's Dilemma:

Two members of a criminal gang are arrested and imprisoned. Each prisoner is in solitary confinement with no means of speaking to or exchanging messages with the other. The police admit they don't have enough evidence to convict the pair on the principal charge. They plan to sentence both to a year in prison on a lesser charge. Simultaneously, the police offer each prisoner a Faustian bargain. If he testifies against his partner, he will go free while the partner will get three years in prison on the main charge. Oh, yes, there is a catch ... If both prisoners testify against each other, both will be sentenced to two years in jail. The prisoners are given a little time to think this over, but in no case may either learn what the other has decided until he has irrevocably made his decision. Each is informed that the other prisoner is being offered the very same deal. Each prisoner is concerned only with his own welfare—with minimizing his own prison sentence.[3]

This leads to three different possible outcomes for prisoners A and B:

If A and B both remain silent, they will each serve one year in prison.
If one testifies against the other but the other doesn’t, the one testifying will be set free while the other serves three years in prison.
If A and B testify against each other, they will each serve two years.
Strategy for the prisoner's dilemma
Two prisoners are separated into individual rooms and cannot communicate with each other. It is assumed that both prisoners understand the nature of the game, have no loyalty to each other, and will have no opportunity for retribution or reward outside of the game. The normal game is shown below:[4]

Prisoner B

Prisoner A
Prisoner B stays silent
(cooperates)	Prisoner B testifies
(defects)
Prisoner A stays silent
(cooperates)	Each serves 1 year	Prisoner A: 3 years
Prisoner B: goes free
Prisoner A testifies
(defects)	Prisoner A: goes free
Prisoner B: 3 years	Each serves 2 years
Regardless of what the other decides, each prisoner gets a higher reward by betraying the other ("defecting"). The reasoning involves analyzing both players' best responses: B will either cooperate or defect. If B cooperates, A should defect, because going free is better than serving 1 year. If B defects, A should also defect, because serving 2 years is better than serving 3. So, either way, A should defect since defecting is A's best response regardless of B's strategy. Parallel reasoning will show that B should defect.[5]

Defection always results in a better payoff than cooperation, so it is a strictly dominant strategy for both players. Mutual defection is the only strong Nash equilibrium in the game. Since the collectively ideal result of mutual cooperation is irrational from a self-interested standpoint, this Nash equilibrium is not Pareto efficient.[6]

Generalized form
icon
This section needs additional citations for verification. Please help improve this article by adding citations to reliable sources in this section. Unsourced material may be challenged and removed. (January 2023) (Learn how and when to remove this message)
The structure of the traditional prisoner's dilemma can be generalized from its original prisoner setting. Suppose that the two players are represented by the colors red and blue and that each player chooses to either "cooperate" or "defect".

If both players cooperate, they both receive the reward 
R
{\displaystyle R} for cooperating. If both players defect, they both receive the punishment payoff 
P
{\displaystyle P}. If Blue defects while Red cooperates, then Blue receives the temptation payoff 
T
{\displaystyle T}, while Red receives the "sucker's" payoff, 
S
{\displaystyle S}. Similarly, if Blue cooperates while Red defects, then Blue receives the sucker's payoff 
S
{\displaystyle S}, while Red receives the temptation payoff 
T
{\displaystyle T}.

This can be expressed in normal form:

Canonical prisoner's dilemma payoff matrix
Red
Blue
Cooperate	Defect
Cooperate	
R
R
T
S
Defect	
S
T
P
P
and to be a prisoner's dilemma game in the strong sense, the following condition must hold for the payoffs:

⁠
T
>
R
>
P
>
S
{\displaystyle T>R>P>S}⁠
The payoff relationship ⁠
R
>
P
{\displaystyle R>P}⁠ implies that mutual cooperation is superior to mutual defection, while the payoff relationships ⁠
T
>
R
{\displaystyle T>R}⁠ and ⁠
P
>
S
{\displaystyle P>S}⁠ imply that defection is the dominant strategy for both agents.[7]

The iterated prisoner's dilemma
If two players play the prisoner's dilemma more than once in succession, remember their opponent's previous actions, and are allowed to change their strategy accordingly, the game is called the iterated prisoner's dilemma.

In addition to the general form above, the iterative version also requires that ⁠
2
R
>
T
+
S
{\displaystyle 2R>T+S}⁠, to prevent alternating cooperation and defection giving a greater reward than mutual cooperation.

The iterated prisoner's dilemma is fundamental to some theories of human cooperation and trust. Assuming that the game effectively models transactions between two people that require trust, cooperative behavior in populations can be modeled by a multi-player iterated version of the game. In 1975, Grofman and Pool estimated the count of scholarly articles devoted to it at over 2,000. The iterated prisoner's dilemma is also called the "peace-war game".[8][9] Several variants of the iterated game have been studied, including a version in which players have an exit option after each round.[10]

General strategy
If the iterated prisoner's dilemma is played a finite number of times and both players know this, then the dominant strategy and Nash equilibrium is to defect in all rounds. The proof is inductive: one might as well defect on the last turn, since the opponent will not have a chance to later retaliate. Therefore, both will defect on the last turn. Thus, the player might as well defect on the second-to-last turn, since the opponent will defect on the last no matter what is done, and so on. The same applies if the game length is unknown but has a known upper limit.[citation needed]

For cooperation to emerge between rational players, the number of rounds must be unknown or infinite. In that case, "always defect" may no longer be a dominant strategy. As shown by Robert Aumann in a 1959 paper,[11] rational players repeatedly interacting for indefinitely long games can sustain cooperation. Specifically, a player may be less willing to cooperate if their counterpart did not cooperate many times, which causes disappointment. Conversely, as time elapses, the likelihood of cooperation tends to rise, owing to the establishment of a "tacit agreement" among participating players. In experimental situations, cooperation can occur even when both participants know how many iterations will be played.[12]

According to a 2019 experimental study in the American Economic Review that tested what strategies real-life subjects used in iterated prisoner's dilemma situations with perfect monitoring, the majority of chosen strategies were always to defect, tit-for-tat, and grim trigger. Which strategy the subjects chose depended on the parameters of the game.[13]

Axelrod's tournament and successful strategy conditions
Interest in the iterated prisoner's dilemma was kindled by Robert Axelrod in his 1984 book The Evolution of Cooperation, in which he reports on a tournament that he organized of the N-step prisoner's dilemma (with N fixed) in which participants have to choose their strategy repeatedly and remember their previous encounters. Axelrod invited academic colleagues from around the world to devise computer strategies to compete in an iterated prisoner's dilemma tournament. The programs that were entered varied widely in algorithmic complexity, initial hostility, capacity for forgiveness, and so forth.

Axelrod discovered that when these encounters were repeated over a long period of time with many players, each with different strategies, greedy strategies tended to do very poorly in the long run while more altruistic strategies did better, as judged purely by self-interest. He used this to show a possible mechanism for the evolution of altruistic behavior from mechanisms that are initially purely selfish, by natural selection.

The winning deterministic strategy was tit for tat, developed and entered into the tournament by Anatol Rapoport. It was the simplest of any program entered, containing only four lines of BASIC,[14] and won the contest. The strategy is simply to cooperate on the first iteration of the game; after that, the player does what his or her opponent did on the previous move.[15] Depending on the situation, a slightly better strategy can be "tit for tat with forgiveness": when the opponent defects, on the next move, the player sometimes cooperates anyway, with a small probability (around 1–5%, depending on the lineup of opponents). This allows for occasional recovery from getting trapped in a cycle of defections.

After analyzing the top-scoring strategies, Axelrod stated several conditions necessary for a strategy to succeed:[16]

Nice: The strategy will not be the first to defect (this is sometimes referred to as an "optimistic" algorithm[by whom?]), i.e., it will not "cheat" on its opponent for purely self-interested reasons first. Almost all the top-scoring strategies were nice.[a]
Retaliating: The strategy must sometimes retaliate. An example of a non-retaliating strategy is Always Cooperate, a very bad choice that will frequently be exploited by "nasty" strategies.
Forgiving: Successful strategies must be forgiving. Though players will retaliate, they will cooperate again if the opponent does not continue to defect. This can stop long runs of revenge and counter-revenge, maximizing points.[b]
Non-envious: The strategy must not strive to score more than the opponent.
In contrast to the one-time prisoner's dilemma game, the optimal strategy in the iterated prisoner's dilemma depends upon the strategies of likely opponents, how they will react to defections and cooperation, and the discounting of future payoffs. For example, if a population consists entirely of players who always defect, except for one who follows the tit-for-tat strategy, that person is at a slight disadvantage because of the loss on the first turn. In such a population, the optimal strategy is to defect every time. More generally, given a population with a certain percentage of always-defectors with the rest being tit-for-tat players, the optimal strategy depends on the percentage and number of iterations played.[citation needed]

Other strategies
Deriving the optimal strategy is generally done in two ways:

Bayesian Nash equilibrium: If the statistical distribution of opposing strategies can be determined an optimal counter-strategy can be derived analytically.[c]
Monte Carlo simulations of populations have been made, where individuals with low scores die off, and those with high scores reproduce (a genetic algorithm for finding an optimal strategy). The mix of algorithms in the final population generally depends on the mix in the initial population. The introduction of mutation (random variation during reproduction) lessens the dependency on the initial population; empirical experiments with such systems tend to produce tit-for-tat players,[clarification needed] but no analytic proof exists that this will always occur.[20]
In the strategy called win-stay, lose-switch, faced with a failure to cooperate, the player switches strategy the next turn.[21] In certain circumstances,[specify] Pavlov beats all other strategies by giving preferential treatment to co-players using a similar strategy.

Although tit-for-tat is considered the most robust basic strategy, a team from Southampton University in England introduced a more successful strategy at the 20th-anniversary iterated prisoner's dilemma competition. It relied on collusion between programs to achieve the highest number of points for a single program. The university submitted 60 programs to the competition, which were designed to recognize each other through a series of five to ten moves at the start.[22] Once this recognition was made, one program would always cooperate and the other would always defect, assuring the maximum number of points for the defector. If the program realized that it was playing a non-Southampton player, it would continuously defect in an attempt to minimize the competing program's score. As a result, the 2004 Prisoners' Dilemma Tournament results show University of Southampton's strategies in the first three places (and a number of positions towards the bottom), despite having fewer wins and many more losses than the GRIM strategy. The Southampton strategy takes advantage of the fact that multiple entries were allowed in this particular competition and that a team's performance was measured by that of the highest-scoring player (meaning that the use of self-sacrificing players was a form of minmaxing).

Because of this new rule, this competition also has little theoretical significance when analyzing single-agent strategies as compared to Axelrod's seminal tournament. But it provided a basis for analyzing how to achieve cooperative strategies in multi-agent frameworks, especially in the presence of noise.

Long before this new-rules tournament was played, Richard Dawkins, in his book The Selfish Gene, pointed out the possibility of such strategies winning if multiple entries were allowed, but wrote that Axelrod would most likely not have allowed them if they had been submitted. Such strategies also circumvent the rule against communication between players: the Southampton programs' "ten-move dance" allowed them to recognize one another, reinforcing how valuable communication can be in shifting the balance of the game.

Even without implicit collusion between software strategies, tit-for-tat is not always the absolute winner of any given tournament; more precisely, its long-run results over a series of tournaments outperform its rivals, but this does not mean it is the most successful in the short term. The same applies to tit-for-tat with forgiveness and other optimal strategies.

This can also be illustrated using the Darwinian ESS simulation. In such a simulation, tit-for-tat will almost always come to dominate, though nasty strategies will drift in and out of the population because a tit-for-tat population is penetrable by non-retaliating nice strategies, which in turn are easy prey for the nasty strategies. Dawkins showed that here, no static mix of strategies forms a stable equilibrium, and the system will always oscillate between bounds.[citation needed]

Stochastic iterated prisoner's dilemma
In a stochastic iterated prisoner's dilemma game, strategies are specified in terms of "cooperation probabilities".[23] In an encounter between player X and player Y, X's strategy is specified by a set of probabilities P of cooperating with Y. P is a function of the outcomes of their previous encounters or some subset thereof. If P is a function of only their most recent n encounters, it is called a "memory-n" strategy. A memory-1 strategy is then specified by four cooperation probabilities: 
P
=
{
P
c
c
,
P
c
d
,
P
d
c
,
P
d
d
}
{\displaystyle P=\{P_{cc},P_{cd},P_{dc},P_{dd}\}}, where Pcd is the probability that X will cooperate in the present encounter given that the previous encounter was characterized by X cooperating and Y defecting. If each of the probabilities are either 1 or 0, the strategy is called deterministic. An example of a deterministic strategy is the tit-for-tat strategy written as 
P
=
{
1
,
0
,
1
,
0
}
{\displaystyle P=\{1,0,1,0\}}, in which X responds as Y did in the previous encounter. Another is the win-stay, lose switch strategy written as 
P
=
{
1
,
0
,
0
,
1
}
{\displaystyle P=\{1,0,0,1\}}. It has been shown that for any memory-n strategy there is a corresponding memory-1 strategy that gives the same statistical results, so that only memory-1 strategies need be considered.[23]

If 
P
{\displaystyle P} is defined as the above 4-element strategy vector of X and 
Q
=
{
Q
c
c
,
Q
c
d
,
Q
d
c
,
Q
d
d
}
{\displaystyle Q=\{Q_{cc},Q_{cd},Q_{dc},Q_{dd}\}} as the 4-element strategy vector of Y (where the indices are from Y's point of view), a transition matrix M may be defined for X whose ij-th entry is the probability that the outcome of a particular encounter between X and Y will be j given that the previous encounter was i, where i and j are one of the four outcome indices: cc, cd, dc, or dd. For example, from X's point of view, the probability that the outcome of the present encounter is cd given that the previous encounter was cd is equal to 
M
c
d
,
c
d
=
P
c
d
(
1
−
Q
d
c
)
{\displaystyle M_{cd,cd}=P_{cd}(1-Q_{dc})}. Under these definitions, the iterated prisoner's dilemma qualifies as a stochastic process and M is a stochastic matrix, allowing all of the theory of stochastic processes to be applied.[23]

One result of stochastic theory is that there exists a stationary vector v for the matrix v such that 
v
⋅
M
=
v
{\displaystyle v\cdot M=v}. Without loss of generality, it may be specified that v is normalized so that the sum of its four components is unity. The ij-th entry in 
M
n
{\displaystyle M^{n}} will give the probability that the outcome of an encounter between X and Y will be j given that the encounter n steps previous is i. In the limit as n approaches infinity, M will converge to a matrix with fixed values, giving the long-term probabilities of an encounter producing j independent of i. In other words, the rows of 
M
∞
{\displaystyle M^{\infty }} will be identical, giving the long-term equilibrium result probabilities of the iterated prisoner's dilemma without the need to explicitly evaluate a large number of interactions. It can be seen that v is a stationary vector for 
M
n
{\displaystyle M^{n}} and particularly 
M
∞
{\displaystyle M^{\infty }}, so that each row of 
M
∞
{\displaystyle M^{\infty }} will be equal to v. Thus, the stationary vector specifies the equilibrium outcome probabilities for X. Defining 
S
x
=
{
R
,
S
,
T
,
P
}
{\displaystyle S_{x}=\{R,S,T,P\}} and 
S
y
=
{
R
,
T
,
S
,
P
}
{\displaystyle S_{y}=\{R,T,S,P\}} as the short-term payoff vectors for the {cc,cd,dc,dd} outcomes (from X's point of view), the equilibrium payoffs for X and Y can now be specified as 
s
x
=
v
⋅
S
x
{\displaystyle s_{x}=v\cdot S_{x}} and 
s
y
=
v
⋅
S
y
{\displaystyle s_{y}=v\cdot S_{y}}, allowing the two strategies P and Q to be compared for their long-term payoffs.

Zero-determinant strategies

The relationship between zero-determinant (ZD), cooperating and defecting strategies in the iterated prisoner's dilemma (iterated prisoner's dilemma)
In 2012, William H. Press and Freeman Dyson published a new class of strategies for the stochastic iterated prisoner's dilemma called "zero-determinant" (ZD) strategies.[23] The long term payoffs for encounters between X and Y can be expressed as the determinant of a matrix which is a function of the two strategies and the short term payoff vectors: 
s
x
=
D
(
P
,
Q
,
S
x
)
{\displaystyle s_{x}=D(P,Q,S_{x})} and 
s
y
=
D
(
P
,
Q
,
S
y
)
{\displaystyle s_{y}=D(P,Q,S_{y})}, which do not involve the stationary vector v. Since the determinant function 
s
y
=
D
(
P
,
Q
,
f
)
{\displaystyle s_{y}=D(P,Q,f)} is linear in 
f
{\displaystyle f}, it follows that 
α
s
x
+
β
s
y
+
γ
=
D
(
P
,
Q
,
α
S
x
+
β
S
y
+
γ
U
)
{\displaystyle \alpha s_{x}+\beta s_{y}+\gamma =D(P,Q,\alpha S_{x}+\beta S_{y}+\gamma U)} (where 
U
=
{
1
,
1
,
1
,
1
}
{\displaystyle U=\{1,1,1,1\}}). Any strategies for which 
D
(
P
,
Q
,
α
S
x
+
β
S
y
+
γ
U
)
=
0
{\displaystyle D(P,Q,\alpha S_{x}+\beta S_{y}+\gamma U)=0} are by definition a ZD strategy, and the long-term payoffs obey the relation 
α
s
x
+
β
s
y
+
γ
=
0
{\displaystyle \alpha s_{x}+\beta s_{y}+\gamma =0}.

Tit-for-tat is a ZD strategy which is "fair", in the sense of not gaining advantage over the other player. But the ZD space also contains strategies that, in the case of two players, can allow one player to unilaterally set the other player's score or alternatively force an evolutionary player to achieve a payoff some percentage lower than his own. The extorted player could defect, but would thereby hurt himself by getting a lower payoff. Thus, extortion solutions turn the iterated prisoner's dilemma into a sort of ultimatum game. Specifically, X is able to choose a strategy for which 
D
(
P
,
Q
,
β
S
y
+
γ
U
)
=
0
{\displaystyle D(P,Q,\beta S_{y}+\gamma U)=0}, unilaterally setting sy to a specific value within a particular range of values, independent of Y's strategy, offering an opportunity for X to "extort" player Y (and vice versa). But if X tries to set sx to a particular value, the range of possibilities is much smaller, consisting only of complete cooperation or complete defection.[23]

An extension of the iterated prisoner's dilemma is an evolutionary stochastic iterated prisoner's dilemma, in which the relative abundance of particular strategies is allowed to change, with more successful strategies relatively increasing. This process may be accomplished by having less successful players imitate the more successful strategies, or by eliminating less successful players from the game, while multiplying the more successful ones. It has been shown that unfair ZD strategies are not evolutionarily stable. The key intuition is that an evolutionarily stable strategy must not only be able to invade another population (which extortionary ZD strategies can do) but must also perform well against other players of the same type (which extortionary ZD players do poorly because they reduce each other's surplus).[24]

Theory and simulations confirm that beyond a critical population size, ZD extortion loses out in evolutionary competition against more cooperative strategies, and as a result, the average payoff in the population increases when the population is larger. In addition, there are some cases in which extortioners may even catalyze cooperation by helping to break out of a face-off between uniform defectors and win–stay, lose–switch agents.[25]

While extortionary ZD strategies are not stable in large populations, another ZD class called "generous" strategies is both stable and robust. When the population is not too small, these strategies can supplant any other ZD strategy and even perform well against a broad array of generic strategies for iterated prisoner's dilemma, including win–stay, lose–switch. This was proven specifically for the donation game by Alexander Stewart and Joshua Plotkin in 2013.[26] Generous strategies will cooperate with other cooperative players, and in the face of defection, the generous player loses more utility than its rival. Generous strategies are the intersection of ZD strategies and so-called "good" strategies, which were defined by Ethan Akin to be those for which the player responds to past mutual cooperation with future cooperation and splits expected payoffs equally if he receives at least the cooperative expected payoff.[27] Among good strategies, the generous (ZD) subset performs well when the population is not too small. If the population is very small, defection strategies tend to dominate.[26]

Continuous iterated prisoner's dilemma
Most work on the iterated prisoner's dilemma has focused on the discrete case, in which players either cooperate or defect, because this model is relatively simple to analyze. However, some researchers have looked at models of the continuous iterated prisoner's dilemma, in which players are able to make a variable contribution to the other player. Le and Boyd[28] found that in such situations, cooperation is much harder to evolve than in the discrete iterated prisoner's dilemma. In a continuous prisoner's dilemma, if a population starts off in a non-cooperative equilibrium, players who are only marginally more cooperative than non-cooperators get little benefit from assorting with one another. By contrast, in a discrete prisoner's dilemma, tit-for-tat cooperators get a big payoff boost from assorting with one another in a non-cooperative equilibrium, relative to non-cooperators. Since nature arguably offers more opportunities for variable cooperation rather than a strict dichotomy of cooperation or defection, the continuous prisoner's dilemma may help explain why real-life examples of tit-for-tat-like cooperation are extremely rare[29] even though tit-for-tat seems robust in theoretical models.

Real-life examples
Many instances of human interaction and natural processes have payoff matrices like the prisoner's dilemma's. It is therefore of interest to the social sciences, such as economics, politics, and sociology, as well as to the biological sciences, such as ethology and evolutionary biology. Many natural processes have been abstracted into models in which living beings are engaged in endless games of prisoner's dilemma.

Environmental studies
In environmental studies, the dilemma is evident in crises such as global climate change. It is argued all countries will benefit from a stable climate, but any single country is often hesitant to curb CO2 emissions. The immediate benefit to any one country from maintaining current behavior is perceived to be greater than the purported eventual benefit to that country if all countries' behavior was changed, therefore explaining the impasse concerning climate-change in 2007.[30]

An important difference between climate-change politics and the prisoner's dilemma is uncertainty; the extent and pace at which pollution can change climate is not known. The dilemma faced by governments is therefore different from the prisoner's dilemma in that the payoffs of cooperation are unknown. This difference suggests that states will cooperate much less than in a real iterated prisoner's dilemma, so that the probability of avoiding a possible climate catastrophe is much smaller than that suggested by a game-theoretical analysis of the situation using a real iterated prisoner's dilemma.[31]

Thomas Osang and Arundhati Nandy provide a theoretical explanation with proofs for a regulation-driven win-win situation along the lines of Michael Porter's hypothesis, in which government regulation of competing firms is substantial.[32]

Animals
Cooperative behavior of many animals can be understood as an example of the iterated prisoner's dilemma. Often animals engage in long-term partnerships; for example, guppies inspect predators cooperatively in groups, and they are thought to punish non-cooperative inspectors.[33]

Vampire bats are social animals that engage in reciprocal food exchange. Applying the payoffs from the prisoner's dilemma can help explain this behavior.[34]

Psychology
In addiction research and behavioral economics, George Ainslie points out that addiction can be cast as an intertemporal prisoner's dilemma problem between the present and future selves of the addict. In this case, "defecting" means relapsing, where not relapsing both today and in the future is by far the best outcome. The case where one abstains today but relapses in the future is the worst outcome: in some sense, the discipline and self-sacrifice involved in abstaining today have been "wasted" because the future relapse means that the addict is right back where they started and will have to start over. Relapsing today and tomorrow is a slightly "better" outcome, because while the addict is still addicted, they haven't put the effort in to trying to stop. The final case, where one engages in the addictive behavior today while abstaining tomorrow, has the problem that (as in other prisoner's dilemmas) there is an obvious benefit to defecting "today", but tomorrow one will face the same prisoner's dilemma, and the same obvious benefit will be present then, ultimately leading to an endless string of defections.[35]

In The Science of Trust, John Gottman defines good relationships as those where partners know not to enter into mutual defection behavior, or at least not to get dynamically stuck there in a loop. In cognitive neuroscience, fast brain signaling associated with processing different rounds may indicate choices at the next round. Mutual cooperation outcomes entail brain activity changes predictive of how quickly a person will cooperate in kind at the next opportunity;[36] this activity may be linked to basic homeostatic and motivational processes, possibly increasing the likelihood of short-cutting into mutual cooperation.

Economics
The prisoner's dilemma has been called the E. coli of social psychology, and it has been used widely to research various topics such as oligopolistic competition and collective action to produce a collective good.[37]

Advertising is sometimes cited as a real example of the prisoner's dilemma. When cigarette advertising was legal in the United States, competing cigarette manufacturers had to decide how much money to spend on advertising. The effectiveness of Firm A's advertising was partially determined by the advertising conducted by Firm B. Likewise, the profit derived from advertising for Firm B is affected by the advertising conducted by Firm A. If both Firm A and Firm B chose to advertise during a given period, then the advertisement from each firm negates the other's, receipts remain constant, and expenses increase due to the cost of advertising. Both firms would benefit from a reduction in advertising. However, should Firm B choose not to advertise, Firm A could benefit greatly by advertising. Nevertheless, the optimal amount of advertising by one firm depends on how much advertising the other undertakes. As the best strategy is dependent on what the other firm chooses there is no dominant strategy, which makes it slightly different from a prisoner's dilemma. The outcome is similar, though, in that both firms would be better off were they to advertise less than in the equilibrium.

Sometimes cooperative behaviors do emerge in business situations. For instance, cigarette manufacturers endorsed the making of laws banning cigarette advertising, understanding that this would reduce costs and increase profits across the industry.[38][d]

Without enforceable agreements, members of a cartel are also involved in a (multi-player) prisoner's dilemma.[39] "Cooperating" typically means agreeing to a price floor, while "defecting" means selling under this minimum level, instantly taking business from other cartel members. Anti-trust authorities want potential cartel members to mutually defect, ensuring the lowest possible prices for consumers.

Sport
Doping in sport has been cited as an example of a prisoner's dilemma. Two competing athletes have the option to use an illegal and/or dangerous drug to boost their performance. If neither athlete takes the drug, then neither gains an advantage. If only one does, then that athlete gains a significant advantage over the competitor, reduced by the legal and/or medical dangers of having taken the drug. But if both athletes take the drug, the benefits cancel out and only the dangers remain, putting them both in a worse position than if neither had doped.[40]

International politics
In international relations theory, the prisoner's dilemma is often used to demonstrate why cooperation fails in situations when cooperation between states is collectively optimal but individually suboptimal.[41][42] A classic example is the security dilemma, whereby an increase in one state's security (such as increasing its military strength) leads other states to fear for their own security out of fear of offensive action.[43] Consequently, security-increasing measures can lead to tensions, escalation or conflict with one or more other parties, producing an outcome which no party truly desires.[44][43][45][46][47] The security dilemma is particularly intense in situations when it is hard to distinguish offensive weapons from defensive weapons, and offense has the advantage in any conflict over defense.[43]

The prisoner's dilemma has frequently been used by realist international relations theorists to demonstrate the why all states (regardless of their internal policies or professed ideology) under international anarchy will struggle to cooperate with one another even when all benefit from such cooperation.

Critics of realism argue that iteration and extending the shadow of the future are solutions to the prisoner's dilemma. When actors play the prisoner's dilemma once, they have incentives to defect, but when they expect to play it repeatedly, they have greater incentives to cooperate.[48]

Multiplayer dilemmas
Many real-life dilemmas involve multiple players.[49] Although metaphorical, Garrett Hardin's tragedy of the commons may be viewed as an example of a multi-player generalization of the prisoner's dilemma: each villager makes a choice for personal gain or restraint. The collective reward for unanimous or frequent defection is very low payoffs and the destruction of the commons.

The commons are not always exploited: William Poundstone, in a book about the prisoner's dilemma, describes a situation in New Zealand where newspaper boxes are left unlocked. It is possible for people to take a paper without paying (defecting), but very few do, feeling that if they do not pay then neither will others, destroying the system.[50] Subsequent research by Elinor Ostrom, winner of the 2009 Nobel Memorial Prize in Economic Sciences, hypothesized that the tragedy of the commons is oversimplified, with the negative outcome influenced by outside influences. Without complicating pressures, groups communicate and manage the commons among themselves for their mutual benefit, enforcing social norms to preserve the resource and achieve the maximum good for the group, an example of effecting the best-case outcome for prisoner's dilemma.[51][52]

Academic settings
The prisoner's dilemma has been used in various academic settings to illustrate the complexities of cooperation and competition. One notable example is the classroom experiment conducted by sociology professor Dan Chambliss at Hamilton College in the 1980s. Starting in 1981, Chambliss proposed that if no student took the final exam, everyone would receive an A, but if even one student took it, those who didn't would receive a zero. In 1988, John Werner, a first-year student, successfully organized his classmates to boycott the exam, demonstrating a practical application of game theory and the prisoner's dilemma concept.[53]

Nearly 25 years later, a similar incident occurred at Johns Hopkins University in 2013. Professor Peter Fröhlich's grading policy scaled final exams according to the highest score, meaning that if everyone received the same score, they would all get an A. Students in Fröhlich's classes organized a boycott of the final exam, ensuring that no one took it. As a result, every student received an A, successfully solving the prisoner's dilemma in a mutually optimal way without iteration.[54][55] These examples highlight how the prisoner's dilemma can be used to explore cooperative behavior and strategic decision-making in educational contexts.

Related games
Closed-bag exchange

The prisoner's dilemma as a briefcase exchange
Douglas Hofstadter[56] suggested that people often find problems such as the prisoner's dilemma problem easier to understand when it is illustrated in the form of a simple game, or trade-off. One of several examples he used was "closed bag exchange":

Two people meet and exchange closed bags, with the understanding that one of them contains money, and the other contains a purchase. Either player can choose to honor the deal by putting into his or her bag what he or she agreed, or he or she can defect by handing over an empty bag.

In game shows
Friend or Foe? is a game show that aired from 2002 to 2003 on the Game Show Network in the US. On the show, three pairs of people compete. When a pair is eliminated, they play a game similar to the prisoner's dilemma to determine how the winnings are split. If they both cooperate (Friend), they share the winnings 50–50. If one cooperates and the other defects (Foe), the defector gets all the winnings and the cooperator gets nothing. If both defect, both leave with nothing. Notice that the reward matrix is slightly different from the standard one given above, as the rewards for the "both defect" and the "cooperate while the opponent defects" cases are identical. This makes the "both defect" case a weak equilibrium, compared with the strict equilibrium in the standard prisoner's dilemma. If a contestant knows that their opponent will vote "Foe", then their own choice does not affect their winnings. In a sense, Friend or Foe has a rewards model between the prisoner's dilemma and the game of Chicken.

This is the rewards matrix:

Pair 2
Pair 1
"Friend"
(cooperate)	"Foe"
(defect)
"Friend"
(cooperate)	
1
1
2
0
"Foe"
(defect)	
0
2
0
0
This payoff matrix has also been used on the British television programs Trust Me, Shafted, The Bank Job, Golden Balls, and The Inner Circle, and on the U.S. game show Take It All, as well as for the winning couple on the reality shows Bachelor Pad and Love Island. A team of economists analyzed data from Golden Balls and found that cooperation was "surprisingly high" for amounts of money that would be consequential in the real world but were comparatively low in the context of the game.[57]

The dilemma is also a Game Mechanic on The Traitors if multiple Traitors remain in the game as finalists. This happened on the second season finale on The Traitors Australia; a three-player variation of the dilemma arose for the three Traitor Finalists. They were given a choice to "share" or "steal" the prize pot. If all three chose to share, each would receive a third of the pot. If one or two traitors chose to steal, those who shared would win nothing and the pot would be divided among those who stole. If all three chose to steal, no one would win anything.

Iterated snowdrift
Researchers from the University of Lausanne and the University of Edinburgh have suggested that the "Iterated Snowdrift Game" may more closely reflect real-world social situations, although this model is actually a chicken game. In this model, the risk of being exploited through defection is lower, and individuals always gain from taking the cooperative choice. The snowdrift game imagines two drivers who are stuck on opposite sides of a snowdrift, each of whom is given the option of shoveling snow to clear a path or remaining in their car. A player's highest payoff comes from leaving the opponent to clear all the snow by themselves, but the opponent is still nominally rewarded for their work.

This may better reflect real-world scenarios, the researchers giving the example of two scientists collaborating on a report, both of whom would benefit if the other worked harder. "But when your collaborator doesn't do any work, it's probably better for you to do all the work yourself. You'll still end up with a completed project."[58][59]

Example snowdrift payouts (A, B)
B 
 A
Cooperates	Defects
Cooperates	500, 500	200, 800
Defects	800, 200	0, 0
Example prisoner's dilemma payouts (A, B)
B 
 A
Cooperates	Defects
Cooperates	500, 500	−200, 1200
Defects	1200, −200	0, 0
Coordination games
Main article: Coordination game
In coordination games, players must coordinate their strategies for a good outcome. An example is two cars that abruptly meet in a blizzard; each must choose whether to swerve left or right. If both swerve left, or both right, the cars do not collide. The local left- and right-hand traffic convention helps to co-ordinate their actions.

Symmetrical co-ordination games include Stag hunt and Bach or Stravinsky.

Asymmetric prisoner's dilemmas
A more general set of games is asymmetric. As in the prisoner's dilemma, the best outcome is cooperation, and there are motives for defection. Unlike the symmetric prisoner's dilemma, though, one player has more to lose and/or more to gain than the other. Some such games have been described as a prisoner's dilemma in which one prisoner has an alibi, hence the term "alibi game".[60]

In experiments, players getting unequal payoffs in repeated games may seek to maximize profits, but only under the condition that both players receive equal payoffs; this may lead to a stable equilibrium strategy in which the disadvantaged player defects every X game, while the other always co-operates. Such behavior may depend on the experiment's social norms around fairness.[61]

Software
Several software packages have been created to run simulations and tournaments of the prisoner's dilemma, some of which have their source code available:

The source code for the second tournament run by Robert Axelrod (written by Axelrod and many contributors in Fortran)[62]
Prison,[63] a library written in Java, last updated in 1998
Axelrod-Python,[64] written in Python
Evoplex,[65] a fast agent-based modeling program released in 2018 by Marcos Cardinot
In fiction
Hannu Rajaniemi set the opening scene of his The Quantum Thief trilogy in a "dilemma prison". The main theme of the series has been described as the "inadequacy of a binary universe" and the ultimate antagonist is a character called the All-Defector. The first book in the series was published in 2010, with the two sequels, The Fractal Prince and The Causal Angel, published in 2012 and 2014, respectively.

A game modeled after the iterated prisoner's dilemma is a central focus of the 2012 video game Zero Escape: Virtue's Last Reward and a minor part in its 2016 sequel Zero Escape: Zero Time Dilemma.

In The Mysterious Benedict Society and the Prisoner's Dilemma by Trenton Lee Stewart, the main characters start by playing a version of the game and escaping from the "prison" altogether. Later, they become actual prisoners and escape once again.

In The Adventure Zone: Balance during The Suffering Game subarc, the player characters are twice presented with the prisoner's dilemma during their time in two liches' domain, once cooperating and once defecting.

In James S. A. Corey's novel Tiamat's Wrath, Colonel Jason Ilich explains the prisoner's dilemma to Winston Duarte's daughter, Teresa, to train her in strategic thinking.[citation needed]

The 2008 film The Dark Knight includes a scene loosely based on the problem in which the Joker rigs two ferries, one containing prisoners and the other containing civilians, arming both groups with the means to detonate the bomb on each other's ferries, threatening to detonate them both if they hesitate.[66][67]

In moral philosophy
The prisoner's dilemma is commonly used as a thinking tool in moral philosophy as an illustration of the potential tension between the benefit of the individual and the benefit of the community.

Both the one-shot and the iterated prisoner's dilemma have applications in moral philosophy. Indeed, many of the moral situations, such as genocide, are not easily repeated more than once. Moreover, in many situations, the previous rounds' outcomes are unknown to the players, since they are not necessarily the same (e.g. interaction with a panhandler on the street).[68]

The philosopher David Gauthier uses the prisoner's dilemma to show how morality and rationality can conflict.[69]

Some game theorists have criticized the use of the prisoner's dilemma as a thinking tool in moral philosophy.[69] Kenneth Binmore argued that the prisoner's dilemma does not accurately describe the game played by humanity, which he argues is closer to a coordination game. Brian Skyrms shares this perspective. Other game theorists see the prisoner's dilemma as arising out of uncertainty over possible non-dilemma games perceived by the players.[70]

Steven Kuhn suggests that these views may be reconciled by considering that moral behavior can modify the payoff matrix of a game, transforming it from a prisoner's dilemma into other games.[69]

Pure and impure prisoner's dilemma
A prisoner's dilemma is considered "impure" if a mixed strategy may give better expected payoffs than a pure strategy. This creates the interesting possibility that the moral action from a utilitarian perspective (i.e., aiming at maximizing the good of an action) may require randomization of one's strategy, such as cooperating with 80% chance and defecting with 20% chance.[71]

See also
Abilene paradox
Centipede game
Collective action problem
Externality
Folk theorem (game theory)
Free-rider problem
Gift-exchange game
Hobbesian trap
Innocent prisoner's dilemma
Liar Game
Metagame
Optional prisoner's dilemma
Prisoner's dilemma and cooperation
Public goods game
Reciprocal altruism
Rent-seeking
Social preferences
Subjective expected relative similarity
Superrationality
Swift trust theory
Tragedy of the commons
Traveler's dilemma
Unscrupulous diner's dilemma
Notes
 The tournament has two rounds. In the first round, each of the top eight strategies were nice, and not one of the bottom seven were nice. In the second round (strategy designers could take into account the results of the first round), all but one of the top fifteen strategies were nice (and that one ranked eighth). Of the bottom fifteen strategies, all but one were not nice.[17]
 In contrast to strategies like grim trigger (also called Friedman), which is never first to defect, but once the other defects even once, grim trigger defects from then on.[18]
 For example see the 2003 study[19] for discussion of the concept and whether it can apply in real economic or strategic situations.
 This argument for the development of cooperation through trust is given in The Wisdom of Crowds, where it is argued that long-distance capitalism was able to form around a nucleus of Quakers, who always dealt honourably with their business partners (rather than defecting and reneging on promises – a phenomenon that had discouraged earlier long-term unenforceable overseas contracts). It is argued that dealings with reliable merchants allowed the meme for cooperation to spread to other traders, who spread it further until a high degree of cooperation became a profitable strategy in general commerce.
References
 "Prisoner's Dilemma". Stanford Encyclopedia of Philosophy. Retrieved 10 March 2024.
 Poundstone 1993, pp. 8, 117.
 Poundstone 1993, p. 118: "A typical contemporary version of the story goes like this: Two members of a criminal gang are arrested and imprisoned. Each prisoner is in solitary confinement with no means of speaking to or exchanging messages with the other. The police admit they don't have enough evidence to convict the pair on the principal charge. They plan to sentence both to a year in prison on a lesser charge. Simultaneously, the police offer each prisoner a Faustian bargain. If he testifies against his partner, he will go free while the partner will get three years in prison on the main charge. Oh, yes, there is a catch ... If both prisoners testify against each other, both will be sentenced to two years in jail. The prisoners are given a little time to think this over, but in no case may either learn what the other has decided until he has irrevocably made his decision. Each is informed that the other prisoner is being offered the very same deal. Each prisoner is concerned only with his own welfare—with minimizing his own prison sentence."
 Poundstone 1993, p. 118.
 Tucker, Albert W. (1950). A Two-Person Dilemma. Read at the Stanford University Psychology Colloquium. Stanford University. Retrieved 3 February 2026.
 Flood, Merrill M. (1958). "Some Experimental Games". Management Science. 5 (1). INFORMS: 5–26. doi:10.1287/mnsc.5.1.5.
 Fader, Peter S.; Hauser, John R. (September 1988). "Implicit Coalitions in a Generalized Prisoner's Dilemma". Journal of Conflict Resolution. 32 (3): 555. doi:10.1177/0022002788032003008.
 Grofman, Bernard; Pool, Jonathan (January 1977). "How to make cooperation the optimizing strategy in a two-person game". The Journal of Mathematical Sociology. 5 (2): 173–186. doi:10.1080/0022250x.1977.9989871. ISSN 0022-250X.
 Shy, Oz (1995). Industrial Organization: Theory and Applications. Massachusetts Institute of Technology Press. ISBN 978-0262193665. Retrieved February 27, 2013.
 Arend, R.J. & Seale, D.A. (2005). Modeling alliance activity: an iterated prisoners' dilemma with exit option. Strategic Management Journal, 26(11), 1057-1074.
 Aumann, Robert J. (2016-03-02), "16. Acceptable Points in General Cooperative n-Person Games", Contributions to the Theory of Games (AM-40), Volume IV, Princeton University Press, pp. 287–324, doi:10.1515/9781400882168-018, ISBN 978-1-4008-8216-8, retrieved 2024-05-14
 Cooper, Russell; DeJong, Douglas V.; Forsythe, Robert; Ross, Thomas W. (1996). "Cooperation without Reputation: Experimental Evidence from Prisoner's Dilemma Games". Games and Economic Behavior. 12 (2): 187–218. doi:10.1006/game.1996.0013.
 Dal Bó, Pedro; Fréchette, Guillaume R. (2019). "Strategy Choice in the Infinitely Repeated Prisoner's Dilemma". American Economic Review. 109 (11): 3929–3952. doi:10.1257/aer.20181480. ISSN 0002-8282. S2CID 216726890.
 Axelrod (2006), p. 193
 Axelrod (2006), p. 31
 Axelrod (2006), chpt. 6
 Axelrod (2006), pp. 113–114
 Axelrod (2006), p. 36
 Landsberger, Michael; Tsirelson, Boris (2003). "Bayesian Nash equilibrium; a statistical test of the hypothesis" (PDF). Tel Aviv University. Archived from the original (PDF) on 2005-10-02.
 Wu, Jiadong; Zhao, Chengye (2019), Sun, Xiaoming; He, Kun; Chen, Xiaoyun (eds.), "Cooperation on the Monte Carlo Rule: Prisoner's Dilemma Game on the Grid", Theoretical Computer Science, Communications in Computer and Information Science, vol. 1069, Springer Singapore, pp. 3–15, doi:10.1007/978-981-15-0105-0_1, ISBN 978-981-15-0104-3, S2CID 118687103
 Wedekind, C.; Milinski, M. (2 April 1996). "Human cooperation in the simultaneous and the alternating Prisoner's Dilemma: Pavlov versus Generous Tit-for-Tat". Proceedings of the National Academy of Sciences. 93 (7): 2686–2689. Bibcode:1996PNAS...93.2686W. doi:10.1073/pnas.93.7.2686. PMC 39691. PMID 11607644.
 "University of Southampton team wins Prisoner's Dilemma competition" (Press release). University of Southampton. 7 October 2004. Archived from the original on 2014-04-21.
 Press, WH; Dyson, FJ (26 June 2012). "Iterated Prisoner's Dilemma contains strategies that dominate any evolutionary opponent". Proceedings of the National Academy of Sciences of the United States of America. 109 (26): 10409–13. Bibcode:2012PNAS..10910409P. doi:10.1073/pnas.1206569109. PMC 3387070. PMID 22615375.
 Adami, Christoph; Arend Hintze (2013). "Evolutionary instability of Zero Determinant strategies demonstrates that winning isn't everything". Nature Communications. 4 (1): 3. arXiv:1208.2666. Bibcode:2013NatCo...4.2193A. doi:10.1038/ncomms3193. PMC 3741637. PMID 23903782.
 Hilbe, Christian; Martin A. Nowak; Karl Sigmund (April 2013). "Evolution of extortion in Iterated Prisoner's Dilemma games". PNAS. 110 (17): 6913–18. arXiv:1212.1067. Bibcode:2013PNAS..110.6913H. doi:10.1073/pnas.1214834110. PMC 3637695. PMID 23572576.
 Stewart, Alexander J.; Joshua B. Plotkin (2013). "From extortion to generosity, evolution in the Iterated Prisoner's Dilemma". Proceedings of the National Academy of Sciences of the United States of America. 110 (38): 15348–53. Bibcode:2013PNAS..11015348S. doi:10.1073/pnas.1306246110. PMC 3780848. PMID 24003115.
 Akin, Ethan (2013). "Stable Cooperative Solutions for the Iterated Prisoner's Dilemma". p. 9. arXiv:1211.0969 [math.DS]. Bibcode:2012arXiv1211.0969A
 Le S, Boyd R (2007). "Evolutionary Dynamics of the Continuous Iterated Prisoner's Dilemma". Journal of Theoretical Biology. 245 (2): 258–67. Bibcode:2007JThBi.245..258L. doi:10.1016/j.jtbi.2006.09.016. PMID 17125798.
 Hammerstein, P. (2003). Why is reciprocity so rare in social animals? A protestant appeal. In: P. Hammerstein, Editor, Genetic and Cultural Evolution of Cooperation, MIT Press. pp. 83–94.
 "Markets & Data". The Economist. 2007-09-27.
 Rehmeyer, Julie (2012-10-29). "Game theory suggests current climate negotiations won't avert catastrophe". Science News. Society for Science & the Public.
 Osang, Thomas; Nandyyz, Arundhati (August 2003). Environmental Regulation of Polluting Firms: Porter's Hypothesis Revisited (PDF) (paper). Archived (PDF) from the original on 2010-07-02.
 Brosnan, Sarah F.; Earley, Ryan L.; Dugatkin, Lee A. (October 2003). "Observational Learning and Predator Inspection in Guppies ( Poecilia reticulata ): Social Learning in Guppies". Ethology. 109 (10): 823–833. doi:10.1046/j.0179-1613.2003.00928.x.
 Dawkins, Richard (1976). The Selfish Gene. Oxford University Press.
 Ainslie, George (2001). Breakdown of Will. Cambridge University Press. ISBN 978-0-521-59694-7.
 Cervantes Constantino, Garat, Nicolaisen, Paz, Martínez-Montes, Kessel, Cabana, and Gradin (2020). "Neural processing of iterated prisoner's dilemma outcomes indicates next-round choice and speed to reciprocate cooperation". Social Neuroscience. 16 (2): 103–120. doi:10.1080/17470919.2020.1859410. PMID 33297873. S2CID 228087900.
 Axelrod, Robert (1980). "Effective Choice in the Prisoner's Dilemma". The Journal of Conflict Resolution. 24 (1): 3–25. Bibcode:1980JConR..24....3A. doi:10.1177/002200278002400101. ISSN 0022-0027. JSTOR 173932. S2CID 143112198.
 Henriksen, Lisa (March 2012). "Comprehensive tobacco marketing restrictions: promotion, packaging, price and place". Tobacco Control. 21 (2): 147–153. doi:10.1136/tobaccocontrol-2011-050416. PMC 4256379. PMID 22345238.
 Nicholson, Walter (2000). Intermediate microeconomics and its application (8th ed.). Fort Worth, TX: Dryden Press : Harcourt College Publishers. ISBN 978-0-030-25916-6.
 Schneier, Bruce (2012-10-26). "Lance Armstrong and the Prisoners' Dilemma of Doping in Professional Sports". Wired. Wired.com. Retrieved 2012-10-29.
 Snyder, Glenn H. (1971). ""Prisoner's Dilemma" and "Chicken" Models in International Politics". International Studies Quarterly. 15 (1): 66–103. doi:10.2307/3013593. ISSN 0020-8833. JSTOR 3013593.
 Jervis, Robert (1978). "Cooperation under the Security Dilemma". World Politics. 30 (2): 167–214. doi:10.2307/2009958. hdl:2027/uc1.31158011478350. ISSN 1086-3338. JSTOR 2009958. S2CID 154923423.
 Jervis, Robert (1978). "Cooperation Under the Security Dilemma". World Politics. 30 (2): 167–214. doi:10.2307/2009958. hdl:2027/uc1.31158011478350. ISSN 0043-8871. JSTOR 2009958. S2CID 154923423.
 Herz, John H. (1950). Idealist Internationalism and the Security Dilemma. pp. 157–180.
 Snyder, Glenn H. (1984). "The Security Dilemma in Alliance Politics". World Politics. 36 (4): 461–495. doi:10.2307/2010183. ISSN 0043-8871. JSTOR 2010183. S2CID 154759602.
 Jervis, Robert (1976). Perception and Misperception in International Politics. Princeton University Press. pp. 58–113. ISBN 978-0-691-10049-4.
 Glaser, Charles L. (2010). Rational Theory of International Politics. Princeton University Press. ISBN 9780691143729.
 Axelrod, Robert; Hamilton, William D. (1981). "The Evolution of Cooperation". Science. 211 (4489): 1390–1396. Bibcode:1981Sci...211.1390A. doi:10.1126/science.7466396. ISSN 0036-8075. PMID 7466396.
 Gokhale CS, Traulsen A. Evolutionary games in the multiverse. Proceedings of the National Academy of Sciences. 2010 Mar 23. 107(12):5500–04.
 Poundstone 1993, pp. 126–127.
 "The Volokh Conspiracy " Elinor Ostrom and the Tragedy of the Commons". Volokh.com. 2009-10-12. Retrieved 2011-12-17.
 Ostrom, Elinor (2015) [1990]. Governing the Commons: The Evolution of Institutions for Collective Action. Cambridge University Press. doi:10.1017/CBO9781316423936. ISBN 978-1-107-56978-2.
 Rivard, Ry (2013-02-21). "A look back at another successful final exam boycott". Inside Higher Ed. Retrieved 2024-07-12.
 Wolfers, Justin (2013-02-14). "Gaming the System". The New York Times. Retrieved 2024-07-12.
 "Johns Hopkins Students Boycott Final Exam - So Everyone Gets an A". Baltimore Fishbowl. 2013-02-25. Retrieved 2024-07-12.
 Hofstadter, Douglas R. (1985). "Ch.29 The Prisoner's Dilemma Computer Tournaments and the Evolution of Cooperation.". Metamagical Themas: questing for the essence of mind and pattern. Bantam Dell Pub Group. ISBN 978-0-465-04566-2.
 Van den Assem, Martijn J. (January 2012). "Split or Steal? Cooperative Behavior When the Stakes Are Large". Management Science. 58 (1): 2–20. doi:10.1287/mnsc.1110.1413. hdl:1765/31292. S2CID 1371739. SSRN 1592456.
 Zyga, Lisa (2007-10-09). "'Snowdrift' game tops 'Prisoner's Dilemma' in explaining cooperation". Phys.org. Archived from the original on 2024-04-11.
 Kümmerli, Rolf; Colliard, Caroline; Fiechter, Nicolas; Petitpierre, Blaise; Russier, Flavien; Keller, Laurent (2007-09-25). "Human cooperation in social dilemmas: comparing the Snowdrift game with the Prisoner's Dilemma". Proceedings of the Royal Society B: Biological Sciences. 274 (1628). Royal Society: 2965–2970. doi:10.1098/rspb.2007.0793. ISSN 1471-2954. PMC 2291152. PMID 17895227.
 Robinson, D.R.; Goforth, D.J. (May 5, 2004). Alibi games: the Asymmetric Prisoner' s Dilemmas (PDF). Meetings of the Canadian Economics Association, Toronto, June 4–6, 2004. Archived (PDF) from the original on 2004-12-06.
 Beckenkamp, Martin; Hennig-Schmidt, Heike; Maier-Rigaud, Frank P. (March 4, 2007). "Cooperation in Symmetric and Asymmetric Prisoner's Dilemma Games" (PDF). Max Planck Institute for Research on Collective Goods. Archived (PDF) from the original on 2019-09-02.
 available online at http://www-personal.umich.edu/~axe/research/Software/CC/CC2.html
 "Proxy-instIPD/Ipd.frame.HTML successfully working". Archived from the original on 10 October 1999.
 "Axelrod-Python/Axelrod: V4.12.0". GitHub.
 "Evoplex · agent-based modeling on networks". evoplex.org.
 Romain, Lindsey (2018-07-18). "The Dark Knight's only redeemable character is the criminal who saves the ferries". Polygon. Retrieved 2024-01-06.
 "The Dark Knight: Game Theory : Networks Course blog for INFO 2040/CS 2850/Econ 2040/SOC 2090". Retrieved 2024-01-06.
 Kuhn, Steven T. (2004-07-01). "Reflections on Ethics and Game Theory". Synthese. 141 (1): 1–44. doi:10.1023/B:SYNT.0000035846.91195.cb. ISSN 1573-0964.
 Kuhn, Steven (December 2016). "Gauthier and the Prisoner's Dilemma". Dialogue. 55 (4): 659–676. doi:10.1017/S0012217316000603. ISSN 0012-2173.
 Arend, R.J. (2020). The expected prisoner’s dilemma–With rationally arising cooperation. PloS one, 15(9), e0239299.
 Kuhn, Steven T.; Moresi, Serge (October 1995). "Pure and Utilitarian Prisoner's Dilemmas". Economics and Philosophy. 11 (2): 333–343. doi:10.1017/S0266267100003424. ISSN 0266-2671.
Bibliography
Poundstone, William (1993). Prisoner's Dilemma (1st Anchor Books ed.). New York: Anchor. ISBN 0-385-41580-X.
Further reading
Amadae, S. (2016). "Prisoner's Dilemma", Prisoners of Reason. Cambridge University Press, NY, pp. 24–61.
Aumann, Robert (1959). "Acceptable points in general cooperative n-person games". In Luce, R. D.; Tucker, A. W. (eds.). Contributions to the Theory 23 of Games IV. Annals of Mathematics Study. Vol. 40. Princeton NJ: Princeton University Press. pp. 287–324. MR 0104521.
Axelrod, Robert (2006). The Evolution of Cooperation (Revised ed.). Basic Books. ISBN 0-465-00564-0.
Bicchieri, Cristina (1993). Rationality and Coordination. Cambridge University Press.
Chess, David M. (December 1988). "Simulating the evolution of behavior: the iterated prisoners' dilemma problem" (PDF). Complex Systems. 2 (6): 663–70. Archived (PDF) from the original on 2015-05-30.
Collins, Rory W. (March 2022). "The prisoner's dilemma paradox: Rationality, morality, and reciprocity". Think: Philosophy for Everyone. 21 (61): 45–55. doi:10.1017/S1477175621000464.
Dresher, M. (1961). The Mathematics of Games of Strategy: Theory and Applications Prentice-Hall, Englewood Cliffs, NJ.
Greif, A. (2006). Institutions and the Path to the Modern Economy: Lessons from Medieval Trade. Cambridge University Press, Cambridge, UK.
Kopelman, Shirli (February 2020). "Tit for tat and beyond: the legendary work of Anatol Rapoport". Negotiation and Conflict Management Research. 13 (1): 60–84. doi:10.1111/ncmr.12172. hdl:2027.42/153763.
Rapoport, Anatol and Albert M. Chammah (1965). Prisoner's Dilemma. University of Michigan Press.
Schneider, Mark; Shields, Timothy W. (June 2022). "Motives for cooperation in the one-shot prisoner's dilemma". Journal of Behavioral Finance. 23 (4): 438–456. doi:10.1080/15427560.2022.2081974. S2CID 249903572.
External links
Wikimedia Commons logo
Wikimedia Commons has media related to Prisoner's dilemma.
Play the interactive Prisoners Dilemma game
The Bowerbird's Dilemma—The Prisoner's Dilemma in ornithology – mathematical cartoon by Larry Gonick.
Dixit, Avinash; Nalebuff, Barry (2008). "Prisoner's Dilemma". In David R. Henderson (ed.). Concise Encyclopedia of Economics (2nd ed.). Indianapolis: Library of Economics and Liberty. ISBN 978-0865976658. OCLC 237794267.
Dawkins: Nice Guys Finish First
Axelrod—Iterated Prisoner's Dilemma Python library
Nicky Case's Evolution of Trust, an example of the donation game
Iterated Prisoner's Dilemma online game by Wayne Davis
What The Prisoner's Dilemma Reveals About Life, The Universe, and Everything by Veritasium
vte
Paradoxes
vte
Game theory
GlossaryGame theoristsGames
Traditional game theory
Combinatorial game theory
Evolutionary game theory
Mechanism design
Other topics
icon Mathematics portalCommonsWikiProjectCategory
Authority control databases Edit this at Wikidata
Categories: DilemmasEnvironmental studiesInefficiency in game theoryMoral psychologyNon-cooperative gamesSocial psychologySocial science experimentsThought experiments
This page was last edited on 26 February 2026, at 02:22 (UTC).
Text is available under the Creative Commons Attribution-ShareAlike 4.0 License; additional terms may apply. By using this site, you agree to the Terms of Use and Privacy Policy. Wikipedia® is a registered trademark of the Wikimedia Foundation, Inc., a non-profit organization.
Privacy policyAbout WikipediaDisclaimersContact WikipediaLegal & safety contactsCode of ConductDevelopersStatisticsCookie statementMobile view
Wikimedia Foundation
Powered by MediaWiki
