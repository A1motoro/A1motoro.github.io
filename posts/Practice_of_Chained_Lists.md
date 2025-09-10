<h1> Practice of Chained Lists </h1>

**Published:** September 8, 2024  
**Category:** Programming
**Read Time:** 10 min

In the [Modification for Chained List](posts/Modification%20for%20Chained%20List.md) blog, we talked about the theroitic modification for chained lists, including **skip lists**, adding a variable named **freelast** to mark the first available memory and a lot.

Now let's throw all these theorys to real practice:

# CF1154E (Two Teams)
# CF1154E Two Teams

## Problem Discription

There are $ n $ students standing in a row. Two coaches are forming two teams — the first coach chooses the first team and the second coach chooses the second team.

The $ i $ -th student has integer programming skill $ a_i $ . All programming skills are distinct and between $ 1 $ and $ n $ , inclusive.

Firstly, the first coach will choose the student with maximum programming skill among all students not taken into any team, and $ k $ closest students to the left of him and $ k $ closest students to the right of him (if there are less than $ k $ students to the left or to the right, all of them will be chosen). All students that are chosen leave the row and join the first team. Secondly, the second coach will make the same move (but all students chosen by him join the second team). Then again the first coach will make such move, and so on. This repeats until the row becomes empty (i. e. the process ends when each student becomes to some team).

Your problem is to determine which students will be taken into the first team and which students will be taken into the second team.

## Input Format

The first line of the input contains two integers $ n $ and $ k $ ( $ 1 \le k \le n \le 2 \cdot 10^5 $ ) — the number of students and the value determining the range of chosen students during each move, respectively.

The second line of the input contains $ n $ integers $ a_1, a_2, \dots, a_n $ ( $ 1 \le a_i \le n $ ), where $ a_i $ is the programming skill of the $ i $ -th student. It is guaranteed that all programming skills are distinct.

## Output Format

Print a string of $ n $ characters; $ i $ -th character should be 1 if $ i $ -th student joins the first team, or 2 otherwise.
## In/Output Examples
### In/Output Example #1

### Input #1

```
5 2
2 4 5 3 1
```

### Output #1

```
11111
```

### In/Output Example #2

#### Input #2

```
5 1
2 1 3 5 4
```

#### Output #2

```
22111
```

### In/Output Example #3

#### Input #3

```
7 1
7 2 1 3 5 4 6
```

#### Output #3

```
1121122
```

### In/Output Example #4

#### Input #4

```
5 1
2 4 5 3 1
```

#### Output #4

```
21112
```

## Tips

In the first example the first coach chooses the student on a position $ 3 $ , and the row becomes empty (all students join the first team).

In the second example the first coach chooses the student on position $ 4 $ , and the row becomes $ [2, 1] $ (students with programming skills $ [3, 4, 5] $ join the first team). Then the second coach chooses the student on position $ 1 $ , and the row becomes empty (and students with programming skills $ [1, 2] $ join the second team).

In the third example the first coach chooses the student on position $ 1 $ , and the row becomes $ [1, 3, 5, 4, 6] $ (students with programming skills $ [2, 7] $ join the first team). Then the second coach chooses the student on position $ 5 $ , and the row becomes $ [1, 3, 5] $ (students with programming skills $ [4, 6] $ join the second team). Then the first coach chooses the student on position $ 3 $ , and the row becomes $ [1] $ (students with programming skills $ [3, 5] $ join the first team). And then the second coach chooses the remaining student (and the student with programming skill $ 1 $ joins the second team).

In the fourth example the first coach chooses the student on position $ 3 $ , and the row becomes $ [2, 1] $ (students with programming skills $ [3, 4, 5] $ join the first team). Then the second coach chooses the student on position $ 1 $ , and the row becomes empty (and students with programming skills $ [1, 2] $ join the second team).
*I'm having a Caculus class at the moment, it's weird*

## Analysis and Solution