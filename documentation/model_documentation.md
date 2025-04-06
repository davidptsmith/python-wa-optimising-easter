# 🐰 Easter Egg Optimisation Model 🐰

## Model Summary

$$
\begin{aligned}
    \text{Maximize:} \quad &  \sum_{i=1}^{N} \sum_{j=1}^{M} e_j \cdot x_{ij}   \quad & \text{Max total enjoyment}\\[2em]
    \text{Subject to:} \quad 
    & x_{ij} \in \mathbb{Z}_{\geq 0}  \quad  &\text{Real whole numbers}  \\[0.5em]
    & x_{ij} \leq s_{ij} \quad  &\text{Egg supply}\\[0.5em]
    & x_{ij} \leq p_{ij}   \quad  &\text{Child's preference} \\[0.5em]
    &  x_{i, \text{golden}} \geq 1   \quad  &\text{Min golden egg} \\[0.5em]
    & \sum_{j=1}^{M} x_{ij} \leq b_i \quad  &\text{Basket capacity} \\[1.5em]
    & \sum_{j} e_j \cdot x_{ij} \geq E_{\text{min}}    \quad  &\text{Min Enjoyment} \\[1.5em]
    & \sum_{j=1}^{M} x_{ij} \leq r \cdot t_i  \quad  &\text{Time limit} \\[1.5em]
    & \left| \sum_{j=1}^{M} x_{ij} - \sum_{j=1}^{M} x_{kj} \right| \leq \theta_h    \quad & \text{Fairness metric} \\[1.5em]
\end{aligned}
\tag{1.1}
$$

$$
0 \leq x_i \leq 1 \quad \text{for all} \quad i = 1, 2, \ldots, n \quad t = 1, 2, \ldots, T \quad   \forall h \in \text{Households} 
$$

## Sets and Indices
- Let $i \in \{1, \dots, N\}$ be the index for children
- Let $j \in \{1, \dots, M\}$ be the index for egg types
- Let $h \in \{1, \dots, H\}$ be the index for households

## Parameters
- $e_j$: enjoyment score of egg type $j$
- $b_i$: basket capacity for child $i$ (max number of eggs they can carry)
- $t_i$: effective time for child $i$
- $s_{ij}$: available supply of egg type $j$
- $\theta_h$: fairness threshold for household $h$ (maximum allowed difference in total eggs between any two children in the same household)
- $E_{\text{min}}$: minimum required enjoyment score

## Decision Variables
- $x_{ij} \in \mathbb{Z}_{\geq 0}$: number of eggs of type $j$ collected by child $i$

## Objective Function:
Maximise total egg enjoyment:
$$
\max \sum_{i=1}^{N} \sum_{j=1}^{M} e_j \cdot x_{ij}
$$

## Subject to Constraints:

### 🔢 Non-negativity and Integrality:
Constraint: No negative or half eggs can be collected. 
$$
x_{ij} \in \mathbb{Z}_{\geq 0} \quad \forall i, j
$$

💡 Use case: Ensures realistic egg counts.

### 🧺 Basket Capacity (Knapsack):
Constraint: Children can only carry as many eggs as their basket allows 
$$
\sum_{j=1}^{M} x_{ij} \leq b_i \quad \forall i
$$

💡 Use case: Prevents overloading children's baskets.

### ⏱️ Time Limit:
Constraint: Children can only collect eggs within their effective time limit.
$$
\sum_{j=1}^{M} x_{ij} \leq r \cdot t_i \quad \forall i
$$

💡 Use case: Ensures children don't exceed their time limit for collecting eggs.

### 🥚 Egg Supply Limits: 
Constraint: The Easter Bunny only has a certain number of eggs. 
$$
x_{ij} \leq s_{ij} \quad \forall i, j
$$

💡 Use case: Ensures the total number of eggs collected does not exceed the available supply.

### ⚖️ Fairness Constraint: 
Constraint: Ensure the difference in total eggs collected by any two children in the same household is within the fairness threshold.
$$
\left| \sum_{j=1}^{M} x_{ij} - \sum_{j=1}^{M} x_{kj} \right| \leq \theta_h \quad \forall h \in \text{Households}, \forall i, k \in h \text{ with } i < k
$$

💡 Use case: Ensures fairness among children in the same household.

### 🎯 Prioritization / Personal Preference
Constraint: Some children prefer certain types of eggs (e.g., healthier or chocolatey ones).  
$$
x_{ij} \leq p_{ij} \quad \forall i, j
$$
Where $p_{ij}$ is the maximum preference weight (e.g., Child 3 doesn’t like chocolate, so $p_{3, \text{chocolate}} = 0$ ).

💡 Use case: Encourages personalisation or diet-based optimisation.

### 📈 Minimum Enjoyment Threshold
Constraint: Ensure each child collects a minimum enjoyment value.  
$$
\sum_{j} e_j \cdot x_{ij} \geq E_{\text{min}} \quad \forall i
$$ 
Where $e_j$ is enjoyment score, and $E_{\text{min}}$ is a required level.  

💡 Use case: Prevents over-optimisation for value alone—adds fun balance.
