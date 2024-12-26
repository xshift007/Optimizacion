\* Programacion_Cirugias_no_GES *\
Minimize
Función_Objetivo: Completion_0 + Completion_1 + Completion_2 + Completion_3
 + Completion_4 + 0.5 Completion_5 + 0.5 Completion_6 + 0.5 Completion_7
 + 0.5 Completion_8 + 0.5 Completion_9 + 0.5 Delay_0 + 0.5 Delay_1
 + 0.5 Delay_2 + 0.5 Delay_3 + 0.5 Delay_4 + 0.5 Delay_5 + 0.5 Delay_6
 + 0.5 Delay_7 + 0.5 Delay_8 + 0.5 Delay_9 + Ociosidad_Total
Subject To
Asignacion_Unica_0: x_0_0 = 1
Asignacion_Unica_1: x_1_0 = 1
Asignacion_Unica_2: x_2_0 = 1
Asignacion_Unica_3: x_3_0 = 1
Asignacion_Unica_4: x_4_0 = 1
Asignacion_Unica_5: x_5_0 = 1
Asignacion_Unica_6: x_6_0 = 1
Asignacion_Unica_7: x_7_0 = 1
Asignacion_Unica_8: x_8_0 = 1
Asignacion_Unica_9: x_9_0 = 1
Completion_Time_0: Completion_0 - Start_0 = 150
Completion_Time_1: Completion_1 - Start_1 = 150
Completion_Time_2: Completion_2 - Start_2 = 150
Completion_Time_3: Completion_3 - Start_3 = 150
Completion_Time_4: Completion_4 - Start_4 = 150
Completion_Time_5: Completion_5 - Start_5 = 60
Completion_Time_6: Completion_6 - Start_6 = 60
Completion_Time_7: Completion_7 - Start_7 = 60
Completion_Time_8: Completion_8 - Start_8 = 60
Completion_Time_9: Completion_9 - Start_9 = 60
Delay_NonNegative_0: Delay_0 >= 0
Delay_NonNegative_1: Delay_1 >= 0
Delay_NonNegative_2: Delay_2 >= 0
Delay_NonNegative_3: Delay_3 >= 0
Delay_NonNegative_4: Delay_4 >= 0
Delay_NonNegative_5: Delay_5 >= 0
Delay_NonNegative_6: Delay_6 >= 0
Delay_NonNegative_7: Delay_7 >= 0
Delay_NonNegative_8: Delay_8 >= 0
Delay_NonNegative_9: Delay_9 >= 0
Delay_Positive_0: - Completion_0 + Delay_0 >= -840
Delay_Positive_1: - Completion_1 + Delay_1 >= -840
Delay_Positive_2: - Completion_2 + Delay_2 >= -840
Delay_Positive_3: - Completion_3 + Delay_3 >= -840
Delay_Positive_4: - Completion_4 + Delay_4 >= -840
Delay_Positive_5: - Completion_5 + Delay_5 >= -840
Delay_Positive_6: - Completion_6 + Delay_6 >= -840
Delay_Positive_7: - Completion_7 + Delay_7 >= -840
Delay_Positive_8: - Completion_8 + Delay_8 >= -840
Delay_Positive_9: - Completion_9 + Delay_9 >= -840
No_Solapamiento_0_1_0: - Completion_0 + Start_1 - 10000 z_0_1_0 >= -10000
No_Solapamiento_0_2_0: - Completion_0 + Start_2 - 10000 z_0_2_0 >= -10000
No_Solapamiento_0_3_0: - Completion_0 + Start_3 - 10000 z_0_3_0 >= -10000
No_Solapamiento_0_4_0: - Completion_0 + Start_4 - 10000 z_0_4_0 >= -10000
No_Solapamiento_0_5_0: - Completion_0 + Start_5 - 10000 z_0_5_0 >= -10000
No_Solapamiento_0_6_0: - Completion_0 + Start_6 - 10000 z_0_6_0 >= -10000
No_Solapamiento_0_7_0: - Completion_0 + Start_7 - 10000 z_0_7_0 >= -10000
No_Solapamiento_0_8_0: - Completion_0 + Start_8 - 10000 z_0_8_0 >= -10000
No_Solapamiento_0_9_0: - Completion_0 + Start_9 - 10000 z_0_9_0 >= -10000
No_Solapamiento_1_0_0: - Completion_1 + Start_0 - 10000 z_1_0_0 >= -10000
No_Solapamiento_1_2_0: - Completion_1 + Start_2 - 10000 z_1_2_0 >= -10000
No_Solapamiento_1_3_0: - Completion_1 + Start_3 - 10000 z_1_3_0 >= -10000
No_Solapamiento_1_4_0: - Completion_1 + Start_4 - 10000 z_1_4_0 >= -10000
No_Solapamiento_1_5_0: - Completion_1 + Start_5 - 10000 z_1_5_0 >= -10000
No_Solapamiento_1_6_0: - Completion_1 + Start_6 - 10000 z_1_6_0 >= -10000
No_Solapamiento_1_7_0: - Completion_1 + Start_7 - 10000 z_1_7_0 >= -10000
No_Solapamiento_1_8_0: - Completion_1 + Start_8 - 10000 z_1_8_0 >= -10000
No_Solapamiento_1_9_0: - Completion_1 + Start_9 - 10000 z_1_9_0 >= -10000
No_Solapamiento_2_0_0: - Completion_2 + Start_0 - 10000 z_2_0_0 >= -10000
No_Solapamiento_2_1_0: - Completion_2 + Start_1 - 10000 z_2_1_0 >= -10000
No_Solapamiento_2_3_0: - Completion_2 + Start_3 - 10000 z_2_3_0 >= -10000
No_Solapamiento_2_4_0: - Completion_2 + Start_4 - 10000 z_2_4_0 >= -10000
No_Solapamiento_2_5_0: - Completion_2 + Start_5 - 10000 z_2_5_0 >= -10000
No_Solapamiento_2_6_0: - Completion_2 + Start_6 - 10000 z_2_6_0 >= -10000
No_Solapamiento_2_7_0: - Completion_2 + Start_7 - 10000 z_2_7_0 >= -10000
No_Solapamiento_2_8_0: - Completion_2 + Start_8 - 10000 z_2_8_0 >= -10000
No_Solapamiento_2_9_0: - Completion_2 + Start_9 - 10000 z_2_9_0 >= -10000
No_Solapamiento_3_0_0: - Completion_3 + Start_0 - 10000 z_3_0_0 >= -10000
No_Solapamiento_3_1_0: - Completion_3 + Start_1 - 10000 z_3_1_0 >= -10000
No_Solapamiento_3_2_0: - Completion_3 + Start_2 - 10000 z_3_2_0 >= -10000
No_Solapamiento_3_4_0: - Completion_3 + Start_4 - 10000 z_3_4_0 >= -10000
No_Solapamiento_3_5_0: - Completion_3 + Start_5 - 10000 z_3_5_0 >= -10000
No_Solapamiento_3_6_0: - Completion_3 + Start_6 - 10000 z_3_6_0 >= -10000
No_Solapamiento_3_7_0: - Completion_3 + Start_7 - 10000 z_3_7_0 >= -10000
No_Solapamiento_3_8_0: - Completion_3 + Start_8 - 10000 z_3_8_0 >= -10000
No_Solapamiento_3_9_0: - Completion_3 + Start_9 - 10000 z_3_9_0 >= -10000
No_Solapamiento_4_0_0: - Completion_4 + Start_0 - 10000 z_4_0_0 >= -10000
No_Solapamiento_4_1_0: - Completion_4 + Start_1 - 10000 z_4_1_0 >= -10000
No_Solapamiento_4_2_0: - Completion_4 + Start_2 - 10000 z_4_2_0 >= -10000
No_Solapamiento_4_3_0: - Completion_4 + Start_3 - 10000 z_4_3_0 >= -10000
No_Solapamiento_4_5_0: - Completion_4 + Start_5 - 10000 z_4_5_0 >= -10000
No_Solapamiento_4_6_0: - Completion_4 + Start_6 - 10000 z_4_6_0 >= -10000
No_Solapamiento_4_7_0: - Completion_4 + Start_7 - 10000 z_4_7_0 >= -10000
No_Solapamiento_4_8_0: - Completion_4 + Start_8 - 10000 z_4_8_0 >= -10000
No_Solapamiento_4_9_0: - Completion_4 + Start_9 - 10000 z_4_9_0 >= -10000
No_Solapamiento_5_0_0: - Completion_5 + Start_0 - 10000 z_5_0_0 >= -10000
No_Solapamiento_5_1_0: - Completion_5 + Start_1 - 10000 z_5_1_0 >= -10000
No_Solapamiento_5_2_0: - Completion_5 + Start_2 - 10000 z_5_2_0 >= -10000
No_Solapamiento_5_3_0: - Completion_5 + Start_3 - 10000 z_5_3_0 >= -10000
No_Solapamiento_5_4_0: - Completion_5 + Start_4 - 10000 z_5_4_0 >= -10000
No_Solapamiento_5_6_0: - Completion_5 + Start_6 - 10000 z_5_6_0 >= -10000
No_Solapamiento_5_7_0: - Completion_5 + Start_7 - 10000 z_5_7_0 >= -10000
No_Solapamiento_5_8_0: - Completion_5 + Start_8 - 10000 z_5_8_0 >= -10000
No_Solapamiento_5_9_0: - Completion_5 + Start_9 - 10000 z_5_9_0 >= -10000
No_Solapamiento_6_0_0: - Completion_6 + Start_0 - 10000 z_6_0_0 >= -10000
No_Solapamiento_6_1_0: - Completion_6 + Start_1 - 10000 z_6_1_0 >= -10000
No_Solapamiento_6_2_0: - Completion_6 + Start_2 - 10000 z_6_2_0 >= -10000
No_Solapamiento_6_3_0: - Completion_6 + Start_3 - 10000 z_6_3_0 >= -10000
No_Solapamiento_6_4_0: - Completion_6 + Start_4 - 10000 z_6_4_0 >= -10000
No_Solapamiento_6_5_0: - Completion_6 + Start_5 - 10000 z_6_5_0 >= -10000
No_Solapamiento_6_7_0: - Completion_6 + Start_7 - 10000 z_6_7_0 >= -10000
No_Solapamiento_6_8_0: - Completion_6 + Start_8 - 10000 z_6_8_0 >= -10000
No_Solapamiento_6_9_0: - Completion_6 + Start_9 - 10000 z_6_9_0 >= -10000
No_Solapamiento_7_0_0: - Completion_7 + Start_0 - 10000 z_7_0_0 >= -10000
No_Solapamiento_7_1_0: - Completion_7 + Start_1 - 10000 z_7_1_0 >= -10000
No_Solapamiento_7_2_0: - Completion_7 + Start_2 - 10000 z_7_2_0 >= -10000
No_Solapamiento_7_3_0: - Completion_7 + Start_3 - 10000 z_7_3_0 >= -10000
No_Solapamiento_7_4_0: - Completion_7 + Start_4 - 10000 z_7_4_0 >= -10000
No_Solapamiento_7_5_0: - Completion_7 + Start_5 - 10000 z_7_5_0 >= -10000
No_Solapamiento_7_6_0: - Completion_7 + Start_6 - 10000 z_7_6_0 >= -10000
No_Solapamiento_7_8_0: - Completion_7 + Start_8 - 10000 z_7_8_0 >= -10000
No_Solapamiento_7_9_0: - Completion_7 + Start_9 - 10000 z_7_9_0 >= -10000
No_Solapamiento_8_0_0: - Completion_8 + Start_0 - 10000 z_8_0_0 >= -10000
No_Solapamiento_8_1_0: - Completion_8 + Start_1 - 10000 z_8_1_0 >= -10000
No_Solapamiento_8_2_0: - Completion_8 + Start_2 - 10000 z_8_2_0 >= -10000
No_Solapamiento_8_3_0: - Completion_8 + Start_3 - 10000 z_8_3_0 >= -10000
No_Solapamiento_8_4_0: - Completion_8 + Start_4 - 10000 z_8_4_0 >= -10000
No_Solapamiento_8_5_0: - Completion_8 + Start_5 - 10000 z_8_5_0 >= -10000
No_Solapamiento_8_6_0: - Completion_8 + Start_6 - 10000 z_8_6_0 >= -10000
No_Solapamiento_8_7_0: - Completion_8 + Start_7 - 10000 z_8_7_0 >= -10000
No_Solapamiento_8_9_0: - Completion_8 + Start_9 - 10000 z_8_9_0 >= -10000
No_Solapamiento_9_0_0: - Completion_9 + Start_0 - 10000 z_9_0_0 >= -10000
No_Solapamiento_9_1_0: - Completion_9 + Start_1 - 10000 z_9_1_0 >= -10000
No_Solapamiento_9_2_0: - Completion_9 + Start_2 - 10000 z_9_2_0 >= -10000
No_Solapamiento_9_3_0: - Completion_9 + Start_3 - 10000 z_9_3_0 >= -10000
No_Solapamiento_9_4_0: - Completion_9 + Start_4 - 10000 z_9_4_0 >= -10000
No_Solapamiento_9_5_0: - Completion_9 + Start_5 - 10000 z_9_5_0 >= -10000
No_Solapamiento_9_6_0: - Completion_9 + Start_6 - 10000 z_9_6_0 >= -10000
No_Solapamiento_9_7_0: - Completion_9 + Start_7 - 10000 z_9_7_0 >= -10000
No_Solapamiento_9_8_0: - Completion_9 + Start_8 - 10000 z_9_8_0 >= -10000
Ociosidad_O_0: Work_O_0 - 150 x_0_0 - 150 x_1_0 - 150 x_2_0 - 150 x_3_0
 - 150 x_4_0 - 60 x_5_0 - 60 x_6_0 - 60 x_7_0 - 60 x_8_0 - 60 x_9_0 = 0
Ociosidad_Total: Ociosidad_Total + Work_O_0 = 1150
Secuenciacion_1_0_0: - x_0_0 + z_0_1_0 + z_0_2_0 + z_0_3_0 + z_0_4_0 + z_0_5_0
 + z_0_6_0 + z_0_7_0 + z_0_8_0 + z_0_9_0 <= 0
Secuenciacion_1_1_0: - x_1_0 + z_1_0_0 + z_1_2_0 + z_1_3_0 + z_1_4_0 + z_1_5_0
 + z_1_6_0 + z_1_7_0 + z_1_8_0 + z_1_9_0 <= 0
Secuenciacion_1_2_0: - x_2_0 + z_2_0_0 + z_2_1_0 + z_2_3_0 + z_2_4_0 + z_2_5_0
 + z_2_6_0 + z_2_7_0 + z_2_8_0 + z_2_9_0 <= 0
Secuenciacion_1_3_0: - x_3_0 + z_3_0_0 + z_3_1_0 + z_3_2_0 + z_3_4_0 + z_3_5_0
 + z_3_6_0 + z_3_7_0 + z_3_8_0 + z_3_9_0 <= 0
Secuenciacion_1_4_0: - x_4_0 + z_4_0_0 + z_4_1_0 + z_4_2_0 + z_4_3_0 + z_4_5_0
 + z_4_6_0 + z_4_7_0 + z_4_8_0 + z_4_9_0 <= 0
Secuenciacion_1_5_0: - x_5_0 + z_5_0_0 + z_5_1_0 + z_5_2_0 + z_5_3_0 + z_5_4_0
 + z_5_6_0 + z_5_7_0 + z_5_8_0 + z_5_9_0 <= 0
Secuenciacion_1_6_0: - x_6_0 + z_6_0_0 + z_6_1_0 + z_6_2_0 + z_6_3_0 + z_6_4_0
 + z_6_5_0 + z_6_7_0 + z_6_8_0 + z_6_9_0 <= 0
Secuenciacion_1_7_0: - x_7_0 + z_7_0_0 + z_7_1_0 + z_7_2_0 + z_7_3_0 + z_7_4_0
 + z_7_5_0 + z_7_6_0 + z_7_8_0 + z_7_9_0 <= 0
Secuenciacion_1_8_0: - x_8_0 + z_8_0_0 + z_8_1_0 + z_8_2_0 + z_8_3_0 + z_8_4_0
 + z_8_5_0 + z_8_6_0 + z_8_7_0 + z_8_9_0 <= 0
Secuenciacion_1_9_0: - x_9_0 + z_9_0_0 + z_9_1_0 + z_9_2_0 + z_9_3_0 + z_9_4_0
 + z_9_5_0 + z_9_6_0 + z_9_7_0 + z_9_8_0 <= 0
Secuenciacion_2_0_0: - x_0_0 + z_1_0_0 + z_2_0_0 + z_3_0_0 + z_4_0_0 + z_5_0_0
 + z_6_0_0 + z_7_0_0 + z_8_0_0 + z_9_0_0 <= 0
Secuenciacion_2_1_0: - x_1_0 + z_0_1_0 + z_2_1_0 + z_3_1_0 + z_4_1_0 + z_5_1_0
 + z_6_1_0 + z_7_1_0 + z_8_1_0 + z_9_1_0 <= 0
Secuenciacion_2_2_0: - x_2_0 + z_0_2_0 + z_1_2_0 + z_3_2_0 + z_4_2_0 + z_5_2_0
 + z_6_2_0 + z_7_2_0 + z_8_2_0 + z_9_2_0 <= 0
Secuenciacion_2_3_0: - x_3_0 + z_0_3_0 + z_1_3_0 + z_2_3_0 + z_4_3_0 + z_5_3_0
 + z_6_3_0 + z_7_3_0 + z_8_3_0 + z_9_3_0 <= 0
Secuenciacion_2_4_0: - x_4_0 + z_0_4_0 + z_1_4_0 + z_2_4_0 + z_3_4_0 + z_5_4_0
 + z_6_4_0 + z_7_4_0 + z_8_4_0 + z_9_4_0 <= 0
Secuenciacion_2_5_0: - x_5_0 + z_0_5_0 + z_1_5_0 + z_2_5_0 + z_3_5_0 + z_4_5_0
 + z_6_5_0 + z_7_5_0 + z_8_5_0 + z_9_5_0 <= 0
Secuenciacion_2_6_0: - x_6_0 + z_0_6_0 + z_1_6_0 + z_2_6_0 + z_3_6_0 + z_4_6_0
 + z_5_6_0 + z_7_6_0 + z_8_6_0 + z_9_6_0 <= 0
Secuenciacion_2_7_0: - x_7_0 + z_0_7_0 + z_1_7_0 + z_2_7_0 + z_3_7_0 + z_4_7_0
 + z_5_7_0 + z_6_7_0 + z_8_7_0 + z_9_7_0 <= 0
Secuenciacion_2_8_0: - x_8_0 + z_0_8_0 + z_1_8_0 + z_2_8_0 + z_3_8_0 + z_4_8_0
 + z_5_8_0 + z_6_8_0 + z_7_8_0 + z_9_8_0 <= 0
Secuenciacion_2_9_0: - x_9_0 + z_0_9_0 + z_1_9_0 + z_2_9_0 + z_3_9_0 + z_4_9_0
 + z_5_9_0 + z_6_9_0 + z_7_9_0 + z_8_9_0 <= 0
Binaries
x_0_0
x_1_0
x_2_0
x_3_0
x_4_0
x_5_0
x_6_0
x_7_0
x_8_0
x_9_0
z_0_1_0
z_0_2_0
z_0_3_0
z_0_4_0
z_0_5_0
z_0_6_0
z_0_7_0
z_0_8_0
z_0_9_0
z_1_0_0
z_1_2_0
z_1_3_0
z_1_4_0
z_1_5_0
z_1_6_0
z_1_7_0
z_1_8_0
z_1_9_0
z_2_0_0
z_2_1_0
z_2_3_0
z_2_4_0
z_2_5_0
z_2_6_0
z_2_7_0
z_2_8_0
z_2_9_0
z_3_0_0
z_3_1_0
z_3_2_0
z_3_4_0
z_3_5_0
z_3_6_0
z_3_7_0
z_3_8_0
z_3_9_0
z_4_0_0
z_4_1_0
z_4_2_0
z_4_3_0
z_4_5_0
z_4_6_0
z_4_7_0
z_4_8_0
z_4_9_0
z_5_0_0
z_5_1_0
z_5_2_0
z_5_3_0
z_5_4_0
z_5_6_0
z_5_7_0
z_5_8_0
z_5_9_0
z_6_0_0
z_6_1_0
z_6_2_0
z_6_3_0
z_6_4_0
z_6_5_0
z_6_7_0
z_6_8_0
z_6_9_0
z_7_0_0
z_7_1_0
z_7_2_0
z_7_3_0
z_7_4_0
z_7_5_0
z_7_6_0
z_7_8_0
z_7_9_0
z_8_0_0
z_8_1_0
z_8_2_0
z_8_3_0
z_8_4_0
z_8_5_0
z_8_6_0
z_8_7_0
z_8_9_0
z_9_0_0
z_9_1_0
z_9_2_0
z_9_3_0
z_9_4_0
z_9_5_0
z_9_6_0
z_9_7_0
z_9_8_0
End
