# Name: pa1.py
# Author(s): Ben Berube and Bo Kulbacki
# Date: 02.20.2023
# Description: Implementation of the Gale-Shapley stable matching algorithm.


def gale_shapley(filename):
    """
    Runs Gale-Shapley algorithm on input
    from file filename.  Format of input file
    given in problem statement.
    Returns a list containing hospitals assigned to each
    student, or None if a student is not assigned to a hospital.
    """

    # Open file and parse contents into corresponding variables and data structures
    f = open(filename, "r")
    line = f.readline().split()
    # Derive number of students and hospitals
    num_hospitals = line[0]
    num_students = line[1]
    # Read next line and create dictionary pairing hospitals to their open positions
    hospital_positions = {}
    student_positions = {}
    """
    key: hospital name/index
    value: (capacity, [ranking of students])
    """
    line = f.readline()
    line_split = line.split()
    for i in range(0, int(num_hospitals)):
        hospital_positions[i] = (int(line_split[i]), [])

    """----PRE PROCESSING----"""

    for i in range(0, int(num_hospitals)):
        line = f.readline()
        line_split = line.split()
        # for (j in range(0, len(line_split))
        hospital_positions[i][1].append(line_split)
        hospital_positions[i] = (hospital_positions[i][0], hospital_positions[i][1].pop())
    # print(hospital_positions)

    for i in range(0, int(num_students)):
        line = f.readline()
        line_split = line.split()
        student_positions[i] = []
        student_positions[i].append(line_split)
        student_positions[i] = (student_positions[i].pop())

    for key in student_positions:
        new_invt_array = []
        for j in range(0, int(num_hospitals)):
            # print(student_positions[key])
            try:
                new_invt_array.append(student_positions[key].index(str(j)))
            except ValueError:
                new_invt_array.append(None)

        student_positions[key] = new_invt_array
        # index in the array is the hospital name, value is its ranking according to student. Hospitals deemed unnacceptable by students hold a value of "None"

    hospitalQ = []
    final_pairing = []
    for i in range(0, int(num_students)):
        final_pairing.append(None)  # student as index
    for i in range(int(num_hospitals)):
        hospitalQ.append(i)

    """    for i in range(int(num_hospitals)):
        while(hospital_positions[i][0]>0):
            hospitalQ.append(i)
            hospital_positions[i] = (hospital_positions[i][0] - 1, hospital_positions[i][1])
    """
    # Close file
    f.close()

    """    ----GALE SHAPLEY STARTS NOW----    
            """

    while len(hospitalQ) > 0:
        h = hospitalQ.pop()
        if hospital_positions[h][0] > 0 and len(hospital_positions[h][1]) != 0:
            s = hospital_positions[h][1].pop(0)
            s = int(s)
            if final_pairing[s] is None:
                # Student is unmatched and accepts hospital (regardless of position)
                if student_positions[s][h] is not None:
                    final_pairing[s] = h
                    # Reduce the number of available positions for particular hospital 'h'
                    hospital_positions[h] = (hospital_positions[h][0] - 1, hospital_positions[h][1])
                    # Add hospital h back to the queue if it still has more open positions
                    num_open_positions = hospital_positions[h][0]
                    if num_open_positions > 0:
                        hospitalQ.append(h)
                else:  # Student does not desire hospital, add hospital back to queue
                    hospitalQ.append(h)

            elif final_pairing[s] is not None:
                # Student is matched, so hospital must compare itself to current matched hospital
                if student_positions[s][h] is not None:
                    # Hospital exists in student priority list
                    h_curr = student_positions[s][final_pairing[s]]  # Retrieve id of current hospital
                    h_prime = student_positions[s][h]
                    if h_curr < h_prime:  # Student prefers current hospital
                        hospitalQ.append(h)
                    else:  # Student prefers new hospital to old

                        # Alter the number of available postions for h_curr and h_prime
                        hospital_positions[h] = (hospital_positions[h][0] - 1, hospital_positions[h][1])
                        hospital_positions[final_pairing[s]] = (hospital_positions[final_pairing[s]][0] + 1, hospital_positions[final_pairing[s]][1])

                        hospitalQ.append(final_pairing[s])  # old hospital gets dropped and must be added to queue
                        # Append new hospital back to queue if more positions are available
                        num_open_positions = hospital_positions[h][0]
                        if num_open_positions > 0:
                            hospitalQ.append(h)

                        # Replace old hospital with preferred new hospital
                        final_pairing[s] = h

                else:  # Student is matched and does not desire new hospital, even after consideration
                    hospitalQ.append(h)

    return final_pairing
