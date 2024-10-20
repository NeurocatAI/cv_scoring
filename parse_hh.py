import requests
from bs4 import BeautifulSoup

def get_html(url: str):
    response = requests.get(
        url,
        headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            },
    )
    # Проверка успешного ответа
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Ошибка загрузки данных с сервера. Статус: {response.status_code}")

def extract_vacancy_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение заголовка вакансии
    title = soup.find('h1', {'data-qa': 'vacancy-title'})
    title = title.text.strip() if title else 'Название вакансии не указано'

    # Извлечение зарплаты
    salary = soup.find('span', {'data-qa': 'vacancy-salary-compensation-type-net'})
    salary = salary.text.strip() if salary else 'Зарплата не указана'

    # Извлечение опыта работы
    experience = soup.find('span', {'data-qa': 'vacancy-experience'})
    experience = experience.text.strip() if experience else 'Опыт работы не указан'

    # Извлечение типа занятости и режима работы
    employment_mode = soup.find('p', {'data-qa': 'vacancy-view-employment-mode'})
    employment_mode = employment_mode.text.strip() if employment_mode else 'Тип занятости не указан'

    # Извлечение компании
    company = soup.find('a', {'data-qa': 'vacancy-company-name'})
    company = company.text.strip() if company else 'Компания не указана'

    # Извлечение местоположения
    location = soup.find('p', {'data-qa': 'vacancy-view-location'})
    location = location.text.strip() if location else 'Местоположение не указано'

    # Извлечение описания вакансии
    description = soup.find('div', {'data-qa': 'vacancy-description'})
    description = description.text.strip() if description else 'Описание не указано'

    # Извлечение ключевых навыков
    skills = [skill.text.strip() for skill in soup.find_all('div', {'class': 'magritte-tag__label___YHV-o_3-0-3'})]
    skills = skills if skills else ['Навыки не указаны']

    # Формирование строки в формате Markdown
    markdown = f"""
# {title}

**Компания:** {company}\n
**Зарплата:** {salary}\n
**Опыт работы:** {experience}\n
**Тип занятости и режим работы:** {employment_mode}\n
**Местоположение:** {location}\n

## Описание вакансии
{description}

## Ключевые навыки
- {'\n- '.join(skills)}
"""

    return markdown.strip()

def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение основных данных кандидата
    name = soup.find('h2', {'data-qa': 'bloko-header-1'})
    name = name.text.strip() if name else 'Имя не указано'

    gender_age = soup.find('p')
    gender_age = gender_age.text.strip() if gender_age else 'Пол и возраст не указаны'

    location = soup.find('span', {'data-qa': 'resume-personal-address'})
    location = location.text.strip() if location else 'Местоположение не указано'

    job_title = soup.find('span', {'data-qa': 'resume-block-title-position'})
    job_title = job_title.text.strip() if job_title else 'Должность не указана'

    job_status = soup.find('span', {'data-qa': 'job-search-status'})
    job_status = job_status.text.strip() if job_status else 'Статус не указан'

    # Извлечение опыта работы
    experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
    experience_items = experience_section.find_all('div', class_='resume-block-item-gap') if experience_section else []
    experiences = []
    for item in experience_items:
        period = item.find('div', class_='bloko-column_s-2')
        duration = item.find('div', class_='bloko-text')
        period_text = period.text.strip() if period else 'Период не указан'
        duration_text = duration.text.strip() if duration else ''
        period_text = period_text.replace(duration_text, f" ({duration_text})") if duration_text else period_text

        company = item.find('div', class_='bloko-text_strong')
        company = company.text.strip() if company else 'Компания не указана'

        position = item.find('div', {'data-qa': 'resume-block-experience-position'})
        position = position.text.strip() if position else 'Позиция не указана'

        description = item.find('div', {'data-qa': 'resume-block-experience-description'})
        description = description.text.strip() if description else 'Описание не указано'

        experiences.append(f"**{period_text}**\n\n*{company}*\n\n**{position}**\n\n{description}\n")

    # Извлечение ключевых навыков
    skills_section = soup.find('div', {'data-qa': 'skills-table'})
    skills = [skill.text.strip() for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})] if skills_section else ['Навыки не указаны']

    # Формирование строки в формате Markdown
    markdown = f"# {name}\n\n"
    markdown += f"**{gender_age}**\n\n"
    markdown += f"**Местоположение:** {location}\n\n"
    markdown += f"**Должность:** {job_title}\n\n"
    markdown += f"**Статус:** {job_status}\n\n"
    markdown += "## Опыт работы\n\n"
    for exp in experiences:
        markdown += exp + "\n"
    markdown += "## Ключевые навыки\n\n"
    markdown += ', '.join(skills) + "\n"

    # Добавляем заголовок для оценки кандидата
    markdown += "\n# Оценка кандидата\n\n"

    return markdown.strip()

def get_candidate_info(url: str):
    html = get_html(url)
    return extract_candidate_data(html)

def get_job_description(url: str):
    html = get_html(url)
    return extract_vacancy_data(html)
