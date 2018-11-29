import numpy as np
import random
import matplotlib.pyplot as plt
available_choice=4# if it cannot stay available_choice=4. If it can stay,
moves=[[-1, 0],[1,0], [0,1], [0,-1], [0, 0]]
moves1=[1, 3, 4, 5, 7, 9, 11, 13, 15, 17, 19, 20, 21, 22, 23, 25, 26, 27, 29]#left
moves2=[0, 2, 3, 4, 6, 8, 10, 12, 14, 16, 18, 19, 20, 21, 22, 24, 25, 26, 28]#right
moves3=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 23]#down
moves4=[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 19, 20, 21, 22, 23, 24, 29]#up
moves5=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
numsList=[]
T=[]
possibility=[]
def bellman(m):#e.g.:m(4,3) 
  cnt=0
  s=[]
  numsList=[]
  for row in range(available_choice):
        numsList.append([])
        for column in range(2):
          num =0
          numsList[row].append(num)
  for i in range(available_choice):
      for j in range(2):
   	    numsList[i][j]=m[j]
   	    numsList[i][j]+=moves[i][j]
      if (numsList[i][0] in range(6)) and (numsList[i][1] in range(5)):	
      		s.append(numsList[i])
      		cnt+=1
  probability=1.0/cnt  
  return probability,s

def player_move(state): #provide all possible moves for player(Considering the wall)
	possible_move=[]
	a,b,c,d=get_point(state)
	temp_point=6*b+a
	if temp_point in moves1:
		possible_move.append(moves[0])
	if temp_point in moves2:
		possible_move.append(moves[1])
	if temp_point in moves3:
		possible_move.append(moves[2])	
	if temp_point in moves4:
		possible_move.append(moves[3])
	if temp_point in moves5:
		possible_move.append(moves[4])
	return possible_move
def get_point(s): #Given state provide the four points
	temp=s//30
	a=temp%6
	b=temp//6
	temp=s%30
	c=temp%6
	d=temp//6
	return a,b,c,d	

def get_state(a,b,s):#Given points provide the state
	return 30*(a+6*b)+s[0]+6*s[1]

def simulation(T,policy):
	initial_state=28
	temp_state=initial_state
	a,b,c,d=get_point(initial_state)
	for i in range(T+1):
		temp_policy=[0,0]
		temp_policy[0]+=best_policy[i][temp_state][0]
		temp_policy[1]+=best_policy[i][temp_state][1]
		a,b,c,d=get_point(temp_state)
		if (a==c) and (b==d):
			#print ('fail')
			#print('T= ', i,'Your position (',a,',', b,')', 'minotaur position (', c, ',', d, ')')
			return 900
		elif (a==4 and b==4) and (state!=868):
			#print('T= ', i,'Your position (',a,',', b,')', 'minotaur position (', c, ',', d, ')')
			#print('T= ', i,'Escape Successfully!!')
			return 901
		else:
			if i==T+1:
				return 900
			#print('T= ', i,'Your position (',a,',', b,')', 'minotaur position (', c, ',', d, ')')

			a+=temp_policy[0]
			b+=temp_policy[1]
			probability,s=bellman([c,d])
			n=1/probability
			rand_num=np.random.random_integers(n)
			c=s[rand_num-1][0]
			d=s[rand_num-1][1]
			temp_state=get_state(a,b,[c,d])
		


def reward(T, state,action):
	probability=0
	s=[]
	a,b,c,d=get_point(state)
	if T==Max_T:
		if (a==4 and b==4) and (state!=868): #state 868 is the state that player and minotaur are both at (4,4)
			u[T,state]=1
			return 1
		else:
			return 0
	else:
		a,b,c,d=get_point(state)
		if ((a==4 and b==4) and (state!=868)):
			u[T,state]=1
			return 1
		else:
			a+=action[0]
			b+=action[1]
			probability,s=bellman([c,d])
			possible_move=player_move(state)
			
			temp_result=0
			for j in range(len(s)):
					temp_result+=1.0*probability*u[T+1,get_state(a,b,s[j])]
					#temp_result=temp_result/30
			return temp_result

for Max_T in range(15):
#Max_T=12
#if 1==1:
	u=np.zeros((Max_T+1,900))
	fail=np.zeros((Max_T+1,900))
	escape=np.zeros((Max_T+1,900))
	best_policy=[]
	for row in range(Max_T+1):
		best_policy.append([])
		for column in range(900):
			best_policy[row].append([0,0])
	for state in range(900):
		u[Max_T,state]=reward(Max_T,state,[0,0])
	for i in reversed(range(Max_T)):
		for state in range(900):
			a,b,c,d=get_point(state)
			if a==c and b==d:
				u[i,state]=0 # In time slot i, it become state fail 
				fail[i,state]=1
			elif (a==4 and b==4) and (state!=868):
				u[i,state]=1  # In time slot i, it become state escape 
				escape[i,state]=1
			else:
				possible_move=player_move(state)
				temp_reward=0
				best_reward=0
				for j in reversed(range(len(possible_move))):
					temp_reward=reward(i,state,possible_move[j])
					if temp_reward>=best_reward:
						best_reward=temp_reward
						best_policy[i][state]=possible_move[j]
					u[i,state]=best_reward
			
	T.append(Max_T)
	possibility.append(u[0,28])
plt.plot(T,possibility)
plt.show()
#success=0
#for i in range(10000):
#	if simulation(Max_T,best_policy)==901:
#		success+=1
#
#print ('Probability of getting out alive is',success/10000)
