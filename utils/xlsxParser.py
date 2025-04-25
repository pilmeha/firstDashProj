from openpyxl import load_workbook

class Group:
    def __init__(self, name, members, score):
        self.name = name
        self.members = members
        self.score = score
        self.minProc = None
        self.minMemb = None

    def addMinProc(self, c):
        self.minProc = c

    def addMinMemb(self, c):
        self.minMemb = c

    def calculateCurrProc(self):
        planS = sum(m.plan for m in self.members)
        currS = sum(m.current for m in self.members)
        return currS / planS if planS else 0

    def calculateCompleteCount(self):
        return sum(1 for m in self.members if m.proc >= 1)

class Member:
    def __init__(self, name, plan, current):
        self.name = name
        self.plan = plan
        self.current = current
        self.proc = current / plan if plan else 0

def parseGroups(sheet):
    gnc, snc, mnc, lnc, pnc, dnc = 'A', 'B', 'C', 'D', 'E', 'F'
    ci = 11
    gi = 0
    g = [Group(sheet[gnc + str(ci)].value, [], sheet[snc + str(ci)].value)]

    while sheet[gnc + str(ci)].value != 'ПЛАН ПО РАЗВИТИЮ':
        sv = sheet[mnc + str(ci)].value
        if sv is not None:
            if sv == 'ИТОГО ПО ГРУППЕ:':
                for i in range(4):
                    if sheet[lnc + str(ci + i)].value == '% выполнения (общий)':
                        g[gi].addMinProc(sheet[pnc + str(ci + i)].value)
                    if sheet[lnc + str(ci + i)].value == 'Количество выполненных разделов':
                        g[gi].addMinMemb(sheet[pnc + str(ci + i)].value)
                if sheet[mnc + str(ci + 3)].value is not None:
                    ci += 2
                else:
                    ci += 3
                gi += 1
                gn = sheet[gnc + str(ci + 1)].value
                if gn != 'ПЛАН ПО РАЗВИТИЮ':
                    g.append(Group(gn, [], sheet[snc + str(ci + 1)].value))
            else:
                planM = sheet[dnc + str(ci)].value or 0
                currM = sheet[dnc + str(ci + 1)].value or 0
                g[gi].members.append(Member(sv, planM, currM))
                if sheet[lnc + str(ci + 3)].value == 'Балл за выполнение':
                    g[gi].addMinProc(1)
                    g[gi].addMinMemb(1)
                    ci += 3
                    gi += 1
                    gn = sheet[gnc + str(ci + 1)].value
                    if gn != 'ПЛАН ПО РАЗВИТИЮ':
                        g.append(Group(gn, [], sheet[snc + str(ci + 1)].value))
        ci += 1

    return g

def load_groups_from_excel(filepath: str, sheet_name="SALES Q1 2025"):
    wb = load_workbook(filepath)
    sheet = wb[sheet_name]
    return parseGroups(sheet)
