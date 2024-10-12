P_D = 0.01  
P_not_D = 1 - P_D  
P_T_given_D = 0.9  
P_T_given_not_D = 0.05  

P_T = (P_T_given_D * P_D) + (P_T_given_not_D * P_not_D)

P_D_given_T = (P_T_given_D * P_D) / P_T

print(f"P(D | T): {P_D_given_T:.4f}")


