# Entropy

$$\text{Entropy(S)} = \sum_{i=1}^{c} - p_i\log_2p_i$$

$$-\frac{param(a)}{param(b)}\log_2\left(\frac{param(a)}{param(b)}\right)$$

Where

$p_i$ is the proportion of instances in class i, and c is the number of classes.

## Golf Play Data

| Outlook  | Temp. | Humidity | Windy | Play Golf |
| -------- | ----- | -------- | ----- | --------- |
| Rainy    | Hot   | High     | False | No        |
| Rainy    | Hot   | High     | True  | No        |
| Overcast | Hot   | High     | False | Yes       |
| Sunny    | Mild  | High     | False | Yes       |
| Sunny    | Cool  | Normal   | False | Yes       |
| Sunny    | Cool  | Normal   | True  | No        |
| Overcast | Cool  | Normal   | True  | Yes       |
| Rainy    | Mild  | High     | False | No        |
| Rainy    | Cool  | Normal   | False | Yes       |
| Sunny    | Mild  | Normal   | False | Yes       |
| Rainy    | Mild  | Normal   | True  | Yes       |
| Overcast | Mild  | High     | True  | Yes       |
| Overcast | Hot   | Normal   | False | Yes       |
| Sunny    | Mild  | High     | True  | No        |

## Play Golf Distribution

| Play Golf | Count |
| --------- | ----- |
| Yes       | 9     |
| No        | 5     |
| Total     | 14    |

### Entropy(Play Golf)

$\text{Entropy(Play Golf)} = \text{Entropy(5, 9)} = $
$-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right) = 1.061019$

## Outlook Distribution

| Outlook  | Play Golf = Yes | Play Golf = No | Total |
| -------- | --------------- | -------------- | ----- |
| Sunny    | 3               | 2              | 5     |
| Overcast | 4               | 0              | 4     |
| Rainy    | 2               | 3              | 5     |
| Total    | 9               | 5              | 14    |

### Entropy(Play Golf, Outlook)

$\text{Entropy(Play Golf, Outlook)} = \text{Prob(Sunny)*Entropy(Sunny) + Prob(Overcast)*Entropy(Overcast) + Prob(Rainy)*Entropy(Rainy)} = $
$\frac{5}{14}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) + 0 + \frac{5}{14}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) = 0.757871$

### Information Gain(Play Golf, Outlook)

$\text{IG(Play Golf, Outlook)} = \text{Entropy(Play Golf) - Entropy(Play Golf, Outlook)} =$
$1.061019 - 0.757871  = 0.303148$

## Temperature Distribution

| Temperature | Play Golf = Yes | Play Golf = No | Total |
| ----------- | --------------- | -------------- | ----- |
| Hot         | 2               | 2              | 4     |
| Mild        | 4               | 2              | 6     |
| Cool        | 3               | 1              | 4     |
| Total       | 9               | 5              | 14    |

### Entropy(Play Golf, Temperature)

$\text{Entropy(Play Golf, Temperature)} = \text{Prob(Hot)*Entropy(Hot) + Prob(Mild)*Entropy(Mild) + Prob(Cool)*Entropy(Cool)} =$
$\frac{4}{14}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) + \frac{6}{14}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) + \frac{4}{14}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) = 1.061019$

### Information Gain(Play Golf, Temperature)

$\text{IG(Play Golf, Temperature)} = \text{Entropy(Play Golf) - Entropy(Play Golf, Temperature)} =$
$1.061019 - 1.061019 = 0$

## Humidity Distribution

| Humidity | Play Golf = Yes | Play Golf = No | Total |
| -------- | --------------- | -------------- | ----- |
| High     | 3               | 4              | 7     |
| Normal   | 6               | 1              | 7     |
| Total    | 9               | 5              | 14    |

### Entropy(Play Golf, Humidity)

$\text{Entropy(Play Golf, Humidity)} = \text{Prob(High)*Entropy(High) + Prob(Normal)*Entropy(Normal)} =$
$\frac{7}{14}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) + \frac{7}{14}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) = 1.061019$

### Information Gain(Play Golf, Humidity)

$\text{IG(Play Golf, Humidity)} = \text{Entropy(Play Golf) - Entropy(Play Golf, Humidity)} =$
$1.061019 - 1.061019 = 0$

## Windy Distribution

| Windy | Play Golf = Yes | Play Golf = No | Total |
| ----- | --------------- | -------------- | ----- |
| False | 6               | 2              | 8     |
| True  | 3               | 3              | 6     |
| Total | 9               | 5              | 14    |

### Entropy(Play Golf, Windy)

$\text{Entropy(Play Golf, Windy)} = \text{Prob(False)*Entropy(False) + Prob(True)*Entropy(True)} =$
$\frac{8}{14}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) + \frac{6}{14}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) = 1.061019$

### Information Gain(Play Golf, Windy)

$\text{IG(Play Golf, Windy)} = \text{Entropy(Play Golf) - Entropy(Play Golf, Windy)} =$
$1.061019 - 1.061019 = 0$

## Summary of Information Gains

| Attribute   | Information Gain        |
| ----------- | ----------------------- |
| Outlook     | $0.303148$ |
| Temperature | $0$ |
| Humidity    | $0$ |
| Windy       | $0$ |

As we can see, the attribute with the highest information gain is **Outlook**, making it the best choice for the root node in a decision tree for this dataset. Now let's find the next best attribute for each branch of outlook.

## Sunny Branch

| Sunny | Count |
| ----- | ----- |
| Yes   | 3     |
| No    | 2     |
| Total | 5     |

### Entropy(Sunny)

$\text{Entropy(Sunny)} = \text{Entropy(3, 2)} =$
$-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right) = 1.061019$

## Temperature Distribution

| Temperature | Play Golf = Yes | Play Golf = No | Total |
| ----------- | --------------- | -------------- | ----- |
| Hot         | 0               | 0              | 0     |
| Mild        | 2               | 1              | 3     |
| Cool        | 1               | 1              | 2     |
| Total       | 3               | 2              | 5     |

### Entropy(Sunny, Temperature)

$\text{Entropy(Sunny, Temperature)} = \text{Prob(Hot)*Entropy(Hot) + Prob(Mild)*Entropy(Mild) + Prob(Cool)*Entropy(Cool)} =$
$0 + \frac{3}{5}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) + \frac{2}{5}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) = 1.061019$

### Information Gain(Sunny, Temperature)

$\text{IG(Sunny, Temperature)} = \text{Entropy(Play Golf | Outlook = Sunny) - Entropy(Sunny, Temperature)} =$
$1.061019 - 1.061019 = 0$

## Humidity Distribution

| Humidity | Play Golf = Yes | Play Golf = No | Total |
| -------- | --------------- | -------------- | ----- |
| High     | 1               | 1              | 2     |
| Normal   | 2               | 1              | 3     |
| Total    | 3               | 2              | 5     |

### Entropy(Sunny, Humidity)

$\text{Entropy(Sunny, Humidity)} = \text{Prob(High)*Entropy(High) + Prob(Normal)*Entropy(Normal)} =$
$\frac{2}{5}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) + \frac{3}{5}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) = 1.061019$

### Information Gain(Sunny, Humidity)

$\text{IG(Sunny, Humidity)} = \text{Entropy(Play Golf | Outlook = Sunny) - Entropy(Sunny, Humidity)} =$
$1.061019 - 1.061019 = 0$

## Windy Distribution

| Windy | Play Golf = Yes | Play Golf = No | Total |
| ----- | --------------- | -------------- | ----- |
| False | 3               | 0              | 3     |
| True  | 0               | 2              | 2     |
| Total | 3               | 2              | 5     |

### Entropy(Sunny, Windy)

$\text{Entropy(Sunny, Windy)} = \text{Prob(False)*Entropy(False) + Prob(True)*Entropy(True)} =$
$\frac{3}{5}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) + \frac{2}{5}\left(-\frac{5}{14}\log_2\left(\frac{5}{14}\right)-\frac{5}{14}\log_2\left(\frac{5}{14}\right)\right) = 1.061019$

### Information Gain(Sunny, Windy)

$\text{IG(Sunny, Windy)} = \text{Entropy(Play Golf | Outlook = Sunny) - Entropy(Sunny, Windy)} =$
$1.061019 - 1.061019 = 0$

## Summary of Information Gains for Sunny Branch

| Attribute   | Information Gain         |
| ----------- | ------------------------ |
| Temperature | $0$ |
| Humidity    | $0$ |
| Windy       | $0$ |

As we can see, the attribute with the highest information gain for the Sunny branch is **Windy**, making it the best choice for the next node in the decision tree for this branch.

## Overcast Branch

For the Overcast branch, all instances result in "Play Golf = Yes". Therefore, no further splits are necessary, and we can directly classify this branch as "Yes".

## Rainy Branch

| Rainy | Count |
| ----- | ----- |
| Yes   | 2     |
| No    | 3     |

...

We can continue this process for the Rainy branch similarly to how we did for the Sunny branch, calculating the information gains for Temperature, Humidity, and Windy, and choosing the best attribute for the next split.

We found out **Humidity** has the highest information gain for the Rainy branch.

## Decision Tree Summary

```mermaid
graph TD;
    A[Outlook]
    A --> B[Sunny]
    A --> C[Overcast]
    A --> D[Rainy]
    B --> E[Windy]
    E --> F[False: Yes]
    E --> G[True: No]
    C --> H[Yes]
    D --> I[Humidity]
    I --> J[High: No]
    I --> K[Normal: Yes]
```
