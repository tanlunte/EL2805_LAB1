import numpy as np
import random
import matplotlib.pyplot as plt
moves=[[-1, 0],[1,0], [0,1], [0,-1], [0, 0]]
def get_state(a,b,c,d):
	return 16*(a+4*b)+c+4*d
def get_action(move):
	 for i in range(len(moves)):
	 	if move==moves[i]:
	 		return i
def get_point(state):
	temp=state//16
	a=temp%4
	b=temp//4
	temp=state%16
	c=temp%4
	d=temp//4
	return a,b,c,d	

def possible_move(m,avilable_choice):
  s=[]
  numsList=[]
  for row in range(avilable_choice):
        numsList.append([])
        for column in range(2):
          num =0
          numsList[row].append(num)
  for i in range(avilable_choice):
      for j in range(2):
   	    numsList[i][j]=m[j]
   	    numsList[i][j]+=moves[i][j]
      if (numsList[i][0] in range(4)) and (numsList[i][1] in range(4)):	
      		s.append(moves[i])
  return s

def get_next_state(state):
	a,b,c,d=get_point(state)
	reward=get_reward(a,b,c,d)
	a,b,current_action=random_move(a,b,5)
	c,d,bla=random_move(c,d,4)
	next_state=get_state(a,b,c,d)
	return next_state,current_action,reward

def random_move(a,b,available_choice):
	possible=[]
	possible=possible_move([a,b],available_choice)
	n=len(possible)
	rand_num=np.random.random_integers(n)
	current_action=possible[rand_num-1]
	a=a+current_action[0]
	b=b+current_action[1]
	return a,b,current_action
def get_reward(a,b,c,d):
	if (a==c) and (b==d) and (a==1) and (b==1):
		r=-9
	elif (a==c) and (b==d):
		r=-10
	elif (a==1) and (b==1):
		r=1
	else:
		r=0
	return r
def get_max_Q(q,s):
	max_Q=-1e10
	best_action=[]
	a,b,c,d=get_point(s) 
	possible=possible_move([a,b],5)
	for move in possible:
		if(q[s,get_action(move)]>max_Q):
			best_action=[]
			best_action.append(move)
			max_Q=q[s,get_action(move)]
		elif(q[s,get_action(move)]==max_Q):
			best_action.append(move)
	rand_num=np.random.random_integers(len(best_action))
	return max_Q,best_action[rand_num-1]


	return max_Q,current_action
def get_sarsa_action(q,state,epsilon):
	rnd=random.random()
	if rnd<=epsilon:
		a,b,c,d=get_point(state)
		a,b,current_action=random_move(a,b,5)
	else:
		max_Q,current_action=get_max_Q(q,state)
	return current_action




def Q_learning(lambda_0):
	t=[]
	Value=[]
	q=np.zeros((256,5))
	n=np.zeros((256,5))
	current_state=get_state(0,0,3,3)		
	for i in range(100000):
		next_state,current_action,r=get_next_state(current_state)
		index_action=get_action(current_action)
		n[current_state,index_action]+=1
		[max_Q,_]=get_max_Q(q,next_state)
		q[current_state,index_action]=q[current_state,index_action]+n[current_state,index_action]**(-2/3)*(r+lambda_0*max_Q-q[current_state,index_action])
		current_state=next_state


		if i%1000==0:
			t.append(i)
			Value.append(q[15,1])	

		if i%10000==0:
			print (i/10000000,'% now')

	return q,t,Value

def SARSA(lambda_0,epsilon):
	t=[]
	Value=[]
	q=np.zeros((256,5))
	n=np.zeros((256,5))
	current_state=get_state(0,0,3,3)
	current_action=get_sarsa_action(q,current_state,epsilon)

	for i in range(10000000):
		next_state=current_state+16*current_action[0]+64*current_action[1]
		next_action=get_sarsa_action(q,next_state,epsilon)
		index_action=get_action(current_action)
		index_next=get_action(next_action)
		a,b,c,d=get_point(current_state)
		r=get_reward(a,b,c,d)
		n[current_state,index_action]+=1
		q[current_state,index_action]=q[current_state,index_action]+n[current_state,index_action]**(-2/3)*(r+lambda_0*q[next_state,index_next]-q[current_state,index_action])
		current_state=next_state
		current_action=next_action
		if i%1000==0:
			t.append(i)
			Value.append(max(q[15,:]))	

		if i%10000==0:
			print (i/100000,'% now')

	return q,t,Value

if __name__ == '__main__':
	#q,t,Value=SARSA(0.8,0.1)
	q1,t1,Value1=SARSA(0.8,0.01)
	q2,t2,Value2=SARSA(0.8,0.1)
	plt.plot(t1,Value1,label='epsilon=0.01')
	plt.plot(t2,Value2,label='epsilon=0.1')
	plt.grid(True)
 
	plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
 

	plt.show()
