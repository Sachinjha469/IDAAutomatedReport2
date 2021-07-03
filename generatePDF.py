import asyncio
import pandas as pd
from pyppeteer import launch
from plottingspiderchart import create_graph

subskill = ['Comprehension', 'Vocabulary', 'Logical Reasoning', 'Verbal Reasoning', 'Information Literacy',
            'Media Literacy', 'Current Affairs', 'Science', 'Sports & Society', 'SST', 'Artificial Intelligence',
            'Information Technology']
user_ids = [44389, 44258, 41727, 42052, 43939, 42996, 39878, 44139, 43024, 42164, 38468, 44287, 40416, 43112, 43277,
            43543, 44611, 40545, 43905, 43209, 43175, 42541, 38507, 43526, 42458, 42803, 43031, 44076, 43779, 43367,
            42656, 43131, 44346, 44323, 42495, 40526, 44257, 44114, 42851, 42722, 43498, 43224, 42679, 42521, 43814,
            39561, 43138, 43852, 43854, 39774, 37855, 43975, 41910, 38098, 43408, 43891, 41991, 42887, 43833, 39140,
            44357, 43413, 44332, 44275, 41590, 39970, 44530, 42355, 38225, 40282, 44065, 42091, 42860, 43857, 42019,
            43757, 42510, 40638, 43965, 44359, 42221, 41783, 43157, 38716, 44452, 41815, 44520, 43839, 43823, 42853,
            41504, 38921, 40199, 43607, 42366, 43932, 42338, 42914, 43798, 43808, 43893, 38490, 42993, 44195, 42026,
            42931, 44157, 43007, 40746, 40728, 42558, 42003, 40497, 43507, 43107, 42084, 42867, 43781, 44005, 43433,
            43794, 40508, 42938, 43559, 39957, 43533, 44516, 43418, 43063, 43796, 43577, 42631, 39849, 43188, 44111,
            44141, 44040, 44085, 42403, 43977, 38948, 42282, 44160, 43899, 38502, 42061, 41770, 41640, 41838, 43843,
            44048, 41553, 43090, 40730, 41865, 44003, 42313, 43775, 39333, 43513, 43835, 42864, 43727, 41948, 44462,
            44192, 42830, 40217, 39760, 43851, 43564, 44319, 39914, 41784, 42462, 44245, 42204, 42675, 43291, 43970,
            41929, 43052, 40522, 43726, 42104, 42764, 43502, 42280, 44246, 40547, 43548, 44132, 40478, 44172, 41759,
            43907, 43084, 43506, 39416, 40074, 44058, 41814, 43037, 43127, 3079, 43582, 40432, 43981, 44106, 44221,
            42437, 44044, 43625, 42105, 42832, 42494, 34715, 43500, 43329, 43208, 43296, 43645, 44301, 40716, 40636,
            43415, 42356, 44418, 40345, 42225, 43253, 41443, 43912, 43378]


async def main():
    info_df = pd.read_csv("Para Article Data - Page 2 (1).csv")
    for index in range(0, info_df.shape[0]):
        print(index)
        stu_user_id=info_df.values[index][0]
        print(stu_user_id)
        filename=info_df.values[index][1]+".pdf"
        # await create_graph()

        # open the HTML page.
        browser = await launch()
        page = await browser.newPage()
        await page.goto('file:///home/sachin/Files/IDAAutomatedReport/htmlfinal/index.html')
        await page.emulateMedia('screen')

        # get the data
        #  Set the data.
        name = info_df.values[index][1]
        school_name = info_df.values[index][2]
        grade = info_df.values[index][3]
        score_str = str(info_df.values[index][4]).split("/")
        obtained_mark, total_marks = int(score_str[0]), int(score_str[1])
        nat_rank = info_df.values[index][5]
        avg_nat_marks = int(info_df.values[index][6])
        #  conversion factor to the percentage
        cnv_factor = 100 / total_marks
        your_score = f"{obtained_mark}/{total_marks}"
        avg_nat_score = f"{avg_nat_marks}/{total_marks}"
        your_score_lbl = str((round(obtained_mark * cnv_factor, 2)))
        avg_score_lbl = str(round(avg_nat_marks * cnv_factor, 2))
        your_score_desc = f"<strong>Your Score:</strong> Total number of correct answers/Total number of questions attempted. Example: Your Score = {obtained_mark}/{total_marks} denotes you answered {obtained_mark} out of {total_marks} questions correctly where {total_marks} is the maximum number of questions in the challenge."
        nat_score_desc = f"<strong>National Average Score:</strong> This is the Average number of correct answers for the respective grade category/Maximum number of questions. For Example: National Score = {avg_nat_marks}/{total_marks} denotes on an average students answered {avg_nat_marks} out of {total_marks} questions correctly."

        # set the data to PDF
        await page.evaluate(f" document.getElementById('name').innerHTML = `{name}`")
        await page.evaluate(f" document.getElementById('school_name').innerHTML = `{school_name}`")
        await page.evaluate(f" document.getElementById('grade').innerHTML = `{grade}`")
        await page.evaluate(f" document.getElementById('nat_rank').innerHTML = `{nat_rank}`")
        await page.evaluate(f" document.getElementById('score').innerHTML = `{your_score}`")
        await page.evaluate(f" document.getElementById('your_score').innerHTML = `{your_score}`")
        await page.evaluate(f" document.getElementById('nat_avg_score').innerHTML = `{avg_nat_score}`")
        await page.evaluate(f" document.getElementById('your_score_desc').innerHTML = `{your_score_desc}`")
        await page.evaluate(f" document.getElementById('nat_score_desc').innerHTML = `{nat_score_desc}`")

        # Plot the bar chart
        score_string = """() =>  {  var chart = new CanvasJS.Chart('chartContainer', { title:{text: 'Score Report'}, axisY: {title: 'Percentage Accuracy', interval: 10}, data: [{dataPoints: [{x: 1, y: %s, label: 'Your Score', indexLabel: '%s'},{ x: 2, y: %s,  label: 'National Average Score', indexLabel: '%s' }]}]});chart.render();}""" % (
            obtained_mark * cnv_factor, your_score_lbl, avg_nat_marks * cnv_factor, avg_score_lbl)
        await page.evaluate(score_string)

        # plot the skill wise table
        skill_df = pd.read_csv("FEC Certificates - Final - Performance across different skills.csv")
        skill_node = ""
        s_header_node = "<thead><tr><td>Skill</td><td>Description</td><td>Right Answer</td><td>Wrong Answer</td></tr></thead>"
        skill_node += s_header_node
        
        for row in range(0, (skill_df.shape[0])):
            if skill_df.values[row][0]==stu_user_id: 
                print(skill_df.values[row][0])        
                skill_node += f"<tr><td>{skill_df.values[row][2]}</td><td>{skill_df.values[row][3]}</td><td>{skill_df.values[row][4]}</td><td>{skill_df.values[row][5]}</td></tr>"
        skill_string = f" document.getElementById('skill_wise').innerHTML = `{skill_node}`"
        await page.evaluate(skill_string)

        list_df = pd.read_csv("FEC Certificates - Sheet6.csv")
        child_node = ""
        index = 0
        q_header_node = "<table><thead><tr><td>S.No</td><td>Skill Name</td><td>Subskill Name</td><td>Question Asked</td><td>Your Answer</td><td>Correct Answer</td><td>Result</td></tr></thead>"
        q_header_node_with_margin = "<table style='margin-top: 50px !important;'><thead><tr><td>S.No</td><td>Skill Name</td><td>Subskill Name</td><td>Question Asked</td><td>Your Answer</td><td>Correct Answer</td><td>Result</td></tr></thead>"
        for row in range(0, (list_df.shape[0])):
            if index % 10 == 0:
                if index != 0:
                    child_node += "</table><p style='page-break-after:always;'/>"
                    child_node += q_header_node_with_margin
                else:
                    child_node += q_header_node
            child_node += f"<tr><td>{list_df.values[row][0]}</td><td>{list_df.values[row][1]}</td><td>{list_df.values[row][2]}</td><td>{list_df.values[row][3]}</td><td>{list_df.values[row][4]}</td><td>{list_df.values[row][5]}</td><td>{list_df.values[row][6]}</td></tr>"
            index += 1
        child_node += "</table><p style='page-break-after:always;'/>"
        insert_string = f" document.getElementById('question_wise').innerHTML = `{child_node}`"
        await page.evaluate(insert_string)
        await page.pdf({'path': filename, 'displayHeaderFooter': True,
                        'margin': {'top': '35', 'right': '10', 'bottom': '35', 'left': '10'},
                        '-webkit-print-color-adjust': True, 'printBackground': True})
        await browser.close()
        break


asyncio.get_event_loop().run_until_complete(main())