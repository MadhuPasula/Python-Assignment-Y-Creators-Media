import pandas as pd

pth = r"C:\Users\sailo\Downloads\Python_Assignment.xlsx"

maths_data = pd.read_excel(pth, sheet_name = 'Maths', engine='openpyxl')
maths_data['% Maths'] = (maths_data['Theory Marks'] + maths_data['Numerical Marks'] + maths_data['Practical Marks'])/3 
maths_data = maths_data[['Roll No', 'Class', '% Maths']]

physics_data = pd.read_excel(pth, sheet_name = 'Physics', engine='openpyxl')
physics_data['% Physics'] = (physics_data['Theory Marks'] + physics_data['Numerical Marks'] + physics_data['Practical Marks'])/3 
physics_data = physics_data[['Roll No', 'Class', '% Physics']]

hindi_data = pd.read_excel(pth, sheet_name = 'Hindi', engine='openpyxl')
hindi_data['% Hindi'] = hindi_data['Marks']
hindi_data = hindi_data[['Roll No', 'Class', '% Hindi']]

economics_data = pd.read_excel(pth, sheet_name = 'Economics', engine='openpyxl')
economics_data['% Economics'] = (economics_data['Theory Marks'] + economics_data['Numerical Marks'])/2 
economics_data = economics_data[['Roll No', 'Class', '% Economics']]

data = pd.merge(maths_data, physics_data, on = ['Roll No', 'Class'], how = 'outer')
data = pd.merge(data, hindi_data, on = ['Roll No', 'Class'], how = 'outer')
data = pd.merge(data, economics_data, on = ['Roll No', 'Class'], how = 'outer')

data = data.sort_values(by=['Roll No', 'Class'], ascending=[True, False])

##
no_of_students = len(data)

##
enrolled_all_subjects = len(data.dropna())

##
classwise_students_count_data = data.groupby('Class')['Roll No'].count().reset_index()
classwise_students_count_data.columns = ['CLass', 'Students Count']
max_num = classwise_students_count_data['Students Count'].max()
classwise_students_max = classwise_students_count_data[classwise_students_count_data['Students Count'] == max_num]

###
data["Total Subjects Enrolled"] = [4 - data.iloc[i,:].isnull().sum() for i in range(len(data))]
copy_data = data.copy()
copy_data = copy_data.fillna(0)
copy_data['Avg Subjects'] = (copy_data['% Maths']+copy_data['% Physics'] + copy_data['% Hindi']+copy_data['% Economics'])/copy_data['Total Subjects Enrolled']
copy_data['Avg Subjects'] = copy_data['Avg Subjects'].apply(int)
max_avg_sub_data = copy_data.groupby('Class')['Avg Subjects'].mean().reset_index()
max_avg_sub_data = max_avg_sub_data.sort_values(by = 'Avg Subjects', ascending = False).head(1)

###
subject_percentage = {col:copy_data[copy_data[col]!=0][col].mean() for col in ['% Maths', '% Physics', '% Hindi', '% Economics']}
highest_subject_percentage = {v:k for k, v in subject_percentage.items()}[max(subject_percentage.values())]
