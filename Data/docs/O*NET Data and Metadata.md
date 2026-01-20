
---

# abilities.md

# Abilities

* [Excel](/dictionary/30.1/excel/abilities.html)
* [Text](/dictionary/30.1/text/abilities.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/abilities.html)
* [Oracle](/dictionary/30.1/oracle/abilities.html)

| **Purpose:** | Provide a mapping of O*NET-SOC codes (occupations) to Ability ratings. |
| **Table Name:** | abilities |
| **Download:** | [11_abilities.sql](/dl_files/database/db_30_1_mysql/11_abilities.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| data_value | Decimal(5,2) | Rating associated with the O*NET-SOC occupation |
| n | Decimal(4,0) | Sample size |
| standard_error | Decimal(7,4) | Standard Error |
| lower_ci_bound | Decimal(7,4) | Lower 95% confidence interval bound |
| upper_ci_bound | Decimal(7,4) | Upper 95% confidence interval bound |
| recommend_suppress | Character(1) | Low precision indicator (Y=yes, N=no) |
| not_relevant | Character(1) | Not relevant for the occupation (Y=yes, N=no) |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

This file contains the Content Model Ability data associated with each O*NET-SOC occupation. It is displayed in 12 tab delimited fields and identified using the column names provided above. Item rating level metadata is provided in columns named n, standard_error, lower_ci_bound, upper_ci_bound, recommend_suppress, not_relevant, date_updated, and domain_source. Refer to **[Appendix 1, *Item Rating Level Statistics - Analyst*](appendix_analyst.html "Appendix 1. Item Rating Level Statistics - Analyst")** for additional information on these items. The 12 fields are represented by one row. There are a total of 92,976 rows of data in this file.

For more information, see:
* [O*NET Analyst Occupational Ratings: Linkage Revisit](https://www.onetcenter.org/reports/LinkageRevisit.html)
* [O*NET Analyst Occupational Abilities Ratings: Procedures Update](https://www.onetcenter.org/reports/AnalystProcUpdate.html)
* [Updating Occupational Ability Profiles with O*NET Content Model Descriptors](https://www.onetcenter.org/reports/UpdateOAP.html)
* [Linking Client Assessment Profiles to O*NET Occupational Profiles Within the O*NET Ability Profiler](https://www.onetcenter.org/reports/AP_Linking.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 | Date and Source columns added |
| 5.1 | Columns added for N, Standard Error, Lower CI Bound, Upper CI Bound, Recommend Suppress, and Not Relevant |
| 6.0 - 28.1 | No structure changes |
| 28.2 | Standard Error, Lower CI Bound, Upper CI Bound expanded from 2 decimal places to 4 |
| 28.3 - 30.1 | No structure changes |

### Data Example - abilities:

| onetsoc_code | element_id | scale_id | data_value | n | standard_error | lower_ci_bound | upper_ci_bound | recommend_suppress | not_relevant | date_updated | domain_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 53-3051.00 | 1.A.1.a.1 | IM | 3.25 | 8 | 0.1637 | 2.9292 | 3.5708 | N | NULL | 2025-08-01 | Analyst |
| 53-3051.00 | 1.A.1.a.1 | LV | 3.38 | 8 | 0.1830 | 3.0164 | 3.7336 | N | N | 2025-08-01 | Analyst |
| 53-3051.00 | 1.A.1.a.2 | IM | 2.75 | 8 | 0.1637 | 2.4292 | 3.0708 | N | NULL | 2025-08-01 | Analyst |
| 53-3051.00 | 1.A.1.a.2 | LV | 3.00 | 8 | 0.0000 | 3.0000 | 3.0000 | N | N | 2025-08-01 | Analyst |
| 53-3051.00 | 1.A.1.a.3 | IM | 3.12 | 8 | 0.1250 | 2.8800 | 3.3700 | N | NULL | 2025-08-01 | Analyst |
| 53-3051.00 | 1.A.1.a.3 | LV | 3.12 | 8 | 0.1250 | 2.8800 | 3.3700 | N | N | 2025-08-01 | Analyst |
| 53-3051.00 | 1.A.1.a.4 | IM | 2.75 | 8 | 0.1637 | 2.4292 | 3.0708 | N | NULL | 2025-08-01 | Analyst |
| 53-3051.00 | 1.A.1.a.4 | LV | 2.75 | 8 | 0.1637 | 2.4292 | 3.0708 | N | N | 2025-08-01 | Analyst |

---

# abilities_to_work_activities.md

# Abilities to Work Activities

* [Excel](/dictionary/30.1/excel/abilities_to_work_activities.html)
* [Text](/dictionary/30.1/text/abilities_to_work_activities.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/abilities_to_work_activities.html)
* [Oracle](/dictionary/30.1/oracle/abilities_to_work_activities.html)

| **Purpose:** | Provide linkages between abilities and relevant work activities. |
| **Table Name:** | abilities_to_work_activities |
| **Download:** | [33_abilities_to_work_activities.sql](/dl_files/database/db_30_1_mysql/33_abilities_to_work_activities.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| abilities_element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| work_activities_element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |

This file contains linkages between abilities and relevant work activities. Occupation-specific ratings for the listed elements may be found in the [*Abilities*](abilities.html "Abilities") and [*Work Activities*](work_activities.html "Work Activities") files. Linkages were developed by a panel of experienced industrial/organizational psychologists, and are used in the development of analyst occupational abilities ratings.

The file is displayed in two tab delimited fields with the columns named Abilities Element ID and Work Activities Element ID. The two fields are represented by one row. There are a total of 381 rows of data in this file.

For more information, see:
* [O*NET Analyst Occupational Abilities Ratings: Procedures Update](https://www.onetcenter.org/reports/AnalystProcUpdate.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 24.2 | Added as a new file |
| 24.3 - 30.1 | No structure changes |

### Data Example - abilities_to_work_activities:

| abilities_element_id | work_activities_element_id |
| --- | --- |
| 1.A.1.a.1 | 4.A.1.a.1 |
| 1.A.1.a.1 | 4.A.1.a.2 |
| 1.A.1.a.1 | 4.A.1.b.1 |
| 1.A.1.a.1 | 4.A.2.a.1 |
| 1.A.1.a.1 | 4.A.2.a.2 |

---

# abilities_to_work_context.md

# Abilities to Work Context

* [Excel](/dictionary/30.1/excel/abilities_to_work_context.html)
* [Text](/dictionary/30.1/text/abilities_to_work_context.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/abilities_to_work_context.html)
* [Oracle](/dictionary/30.1/oracle/abilities_to_work_context.html)

| **Purpose:** | Provide linkages between abilities and relevant work context. |
| **Table Name:** | abilities_to_work_context |
| **Download:** | [34_abilities_to_work_context.sql](/dl_files/database/db_30_1_mysql/34_abilities_to_work_context.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| abilities_element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| work_context_element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |

This file contains linkages between abilities and relevant work context. Occupation-specific ratings for the listed elements may be found in the [*Abilities*](abilities.html "Abilities") and [*Work Context*](work_context.html "Work Context") files. Linkages were developed by a panel of experienced industrial/organizational psychologists, and are used in the development of analyst occupational abilities ratings.

The file is displayed in two tab delimited fields with the columns named Abilities Element ID and Work Context Element ID. The two fields are represented by one row. There are a total of 139 rows of data in this file.

For more information, see:
* [O*NET Analyst Occupational Abilities Ratings: Procedures Update](https://www.onetcenter.org/reports/AnalystProcUpdate.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 24.2 | Added as a new file |
| 24.3 - 30.1 | No structure changes |

### Data Example - abilities_to_work_context:

| abilities_element_id | work_context_element_id |
| --- | --- |
| 1.A.1.a.1 | 4.C.1.a.2.c |
| 1.A.1.a.1 | 4.C.1.a.2.f |
| 1.A.1.a.1 | 4.C.1.a.2.l |
| 1.A.1.a.1 | 4.C.1.a.4 |
| 1.A.1.a.1 | 4.C.1.b.1.e |

---

# alternate_titles.md

# Alternate Titles

* [Excel](/dictionary/30.1/excel/alternate_titles.html)
* [Text](/dictionary/30.1/text/alternate_titles.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/alternate_titles.html)
* [Oracle](/dictionary/30.1/oracle/alternate_titles.html)

| **Purpose:** | Provide alternate occupational titles for O*NET-SOC occupations. |
| **Table Name:** | alternate_titles |
| **Download:** | [29_alternate_titles.sql](/dl_files/database/db_30_1_mysql/29_alternate_titles.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| alternate_title | Character Varying(250) | Alternate occupational title |
| short_title | Character Varying(150) | Short version of alternate title (if applicable) |
| sources | Character Varying(50) | List of source codes — see below |

This file contains job or alternate "lay" titles linked to occupations in the O*NET-SOC classification system. The file was developed to improve keyword searches in several Department of Labor internet applications (i.e., Career InfoNet, O*NET OnLine, and O*NET Code Connector). The file contains occupational titles from existing occupational classification systems, as well as from other diverse sources. When a title contains acronyms, abbreviations, or jargon, the “Short Title” column contains the brief version of the full title. The “Source(s)” column contains a comma delimited list of codes which indicate the source of the title information; the codes are identified below:

| 01 | Associations [i.e., National Retail Federation, Environmental Career Centers (ECC), etc.] |
|---|---|
| 02 | Incumbent Data – O*NET Data Collection |
| 03 | Occupational Code Assignment (OCA) |
| 04 | SOC (i.e., SOC Index, SOC Volume 2, etc.) |
| 05 | State Agencies |
| 06 | US Bureau of Census (e.g., Census Index) |
| 07 | USDOL – BLS (e.g., IT to SOC) |
| 08 | USDOL – ETA (i.e., OPDER, OATELS, ACINET/Fu Associates, DOT, O*NET Center, etc.) |
| 09 | USDOL – User input, web applications (Code Connector, OnLine, and ACINET) |
| 10 | Employer Job Postings |

The file is displayed in four tab delimited fields with the columns named O*NET-SOC Code, Alternate Title, Short Title, and Source(s). The four fields are represented by one row. There are a total of 56,505 rows of data in this file.

For more information, see:
* [O*NET Alternate Titles Procedures](https://www.onetcenter.org/reports/AltTitles.html)
* [A Weighted O*NET Keyword Search (WWS)](https://www.onetcenter.org/reports/WWS.html)
* [Military Transition Search (as used in My Next Move for Veterans)](https://www.onetcenter.org/reports/MilitarySearch.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 20.1 | Added as a new file |
| 20.2 - 21.3 | No structure changes |
| 22.0 | increased "Alternate Title" column from 150 to 250 characters |
| 22.1 - 30.1 | No structure changes |

### Data Example - alternate_titles:

| onetsoc_code | alternate_title | short_title | sources |
| --- | --- | --- | --- |
| 29-2099.00 | Sleep Technician | NULL | 09 |

---

# basic_interests_to_riasec.md

# Basic Interests to RIASEC

* [Excel](/dictionary/30.1/excel/basic_interests_to_riasec.html)
* [Text](/dictionary/30.1/text/basic_interests_to_riasec.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/basic_interests_to_riasec.html)
* [Oracle](/dictionary/30.1/oracle/basic_interests_to_riasec.html)

| **Purpose:** | Provide linkages between each basic occupational interest to relevant general occupational interests. |
| **Table Name:** | basic_interests_to_riasec |
| **Download:** | [38_basic_interests_to_riasec.sql](/dl_files/database/db_30_1_mysql/38_basic_interests_to_riasec.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| basic_interests_element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| riasec_element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |

This file contains linkages between each basic occupational interest to relevant general occupational interests. The file is displayed in two tab delimited fields with the columns named Basic Interests Element ID and RIASEC Element ID. The two fields are represented by one row. There are a total of 53 rows of data in this file.

For more information, see:
* [Updating Vocational Interests Information for the O*NET Content Model](https://www.onetcenter.org/reports/Voc_Interests.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 27.2 | Added as a new file |
| 27.3 - 30.1 | No structure changes |

### Data Example - basic_interests_to_riasec:

| basic_interests_element_id | riasec_element_id |
| --- | --- |
| 1.B.3.a | 1.B.1.a |
| 1.B.3.b | 1.B.1.a |
| 1.B.3.c | 1.B.1.a |
| 1.B.3.d | 1.B.1.a |
| 1.B.3.e | 1.B.1.a |

---

# concat_docs.sh

#!/usr/bin/env bash
set -euo pipefail

src_dir="${1:-.}"
out_file="${2:-all_docs.md}"

if [[ ! -d "$src_dir" ]]; then
  echo "source directory not found: $src_dir" >&2
  exit 1
fi

mkdir -p "$(dirname "$out_file")"

out_abs="$(cd "$(dirname "$out_file")" && pwd)/$(basename "$out_file")"
tmp_file="$(mktemp)"

while IFS= read -r file; do
  file_abs="$(cd "$(dirname "$file")" && pwd)/$(basename "$file")"
  if [[ "$file_abs" == "$out_abs" ]]; then
    continue
  fi
  rel_path="${file#$src_dir/}"
  {
    echo ""
    echo "---"
    echo ""
    echo "# ${rel_path}"
    echo ""
    cat "$file"
    echo ""
  } >> "$tmp_file"
done < <(find "$src_dir" -type f | LC_ALL=C sort)

mv "$tmp_file" "$out_file"
echo "wrote: $out_file"


---

# content_model_reference.md

# Content Model Reference

* [Excel](/dictionary/30.1/excel/content_model_reference.html)
* [Text](/dictionary/30.1/text/content_model_reference.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/content_model_reference.html)
* [Oracle](/dictionary/30.1/oracle/content_model_reference.html)

| **Purpose:** | Provide O*NET Content Model elements. |
| **Table Name:** | content_model_reference |
| **Download:** | [01_content_model_reference.sql](/dl_files/database/db_30_1_mysql/01_content_model_reference.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| element_id | Character Varying(20) | Content Model Outline Position |
| element_name | Character Varying(150) | Content Model Element Name |
| description | Character Varying(1500) | Content Model Element Description |

This file contains the Content Model elements and descriptions. The file is displayed in three tab delimited fields with the columns named Element ID, Element Name, and Description. The three fields are represented by one row. There are a total of 630 rows of data in this file.

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 - 30.1 | No structure changes |

### Data Example - content_model_reference:

| element_id | element_name | description |
| --- | --- | --- |
| 1 | Worker Characteristics | Worker Characteristics |
| 1.A | Abilities | Enduring attributes of the individual that influence performance |
| 1.A.1 | Cognitive Abilities | Abilities that influence the acquisition and application of knowledge in problem solving |
| 1.A.1.a | Verbal Abilities | Abilities that influence the acquisition and application of verbal information in problem solving |
| 1.A.1.a.1 | Oral Comprehension | The ability to listen to and understand information and ideas presented through spoken words and sentences. |

---

# dwa_reference.md

# DWA Reference

* [Excel](/dictionary/30.1/excel/dwa_reference.html)
* [Text](/dictionary/30.1/text/dwa_reference.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/dwa_reference.html)
* [Oracle](/dictionary/30.1/oracle/dwa_reference.html)

| **Purpose:** | Provide each Detailed Work Activity. |
| **Table Name:** | dwa_reference |
| **Download:** | [24_dwa_reference.sql](/dl_files/database/db_30_1_mysql/24_dwa_reference.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| iwa_id | Character Varying(20) | Identifies each Intermediate Work Activity *(see [*IWA Reference*](iwa_reference.html "IWA Reference"))* |
| dwa_id | Character Varying(20) | Identifies each Detailed Work Activity |
| dwa_title | Character Varying(150) | Detailed Work Activity statement |

This file contains each Detailed Work Activity and its corresponding GWA and IWA identifiers. Each DWA is linked to exactly one IWA, which in turn is linked to exactly one Work Activity from the O*NET Content Model. See [*Content Model Reference*](content_model_reference.html "Content Model Reference") and [*IWA Reference*](iwa_reference.html "IWA Reference") for information about these higher-level elements. Each DWA is linked to multiple task statements; see [*Tasks to DWAs*](tasks_to_dwas.html "Tasks to DWAs") for these links.

The file is displayed in four tab delimited fields with the columns named Element ID, IWA ID, DWA ID, and DWA Title. The four fields are represented by one row. There are a total of 2,087 rows of data in this file.

For more information, see:
* [O*NET Work Activities Project Technical Report](https://www.onetcenter.org/reports/DWA_2014.html)
* [Ranking Detailed Work Activities (DWAs) Within O*NET® Occupational Profiles](https://www.onetcenter.org/reports/DWA_Ranking.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 18.1 | Added as a new file |
| 19.0 - 30.1 | No structure changes |

### Data Example - dwa_reference:

| element_id | iwa_id | dwa_id | dwa_title |
| --- | --- | --- | --- |
| 4.A.1.a.1 | 4.A.1.a.1.I01 | 4.A.1.a.1.I01.D01 | Review art or design materials. |
| 4.A.1.a.1 | 4.A.1.a.1.I01 | 4.A.1.a.1.I01.D02 | Study details of musical compositions. |
| 4.A.2.b.2 | 4.A.2.b.2.I14 | 4.A.2.b.2.I14.D06 | Design control systems for mechanical or other equipment. |
| 4.A.4.b.6 | 4.A.4.b.6.I09 | 4.A.4.b.6.I09.D03 | Advise others on health and safety issues. |

---

# education_training_experience.md

# Education, Training, and Experience

* [Excel](/dictionary/30.1/excel/education_training_experience.html)
* [Text](/dictionary/30.1/text/education_training_experience.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/education_training_experience.html)
* [Oracle](/dictionary/30.1/oracle/education_training_experience.html)

| **Purpose:** | Provide a mapping of O*NET-SOC codes (occupations) to Education, Training, and Experience ratings. |
| **Table Name:** | education_training_experience |
| **Download:** | [12_education_training_experience.sql](/dl_files/database/db_30_1_mysql/12_education_training_experience.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| category | Decimal(3,0) | Percent frequency category *(see [*Education, Training, and Experience Categories*](ete_categories.html "Education, Training, and Experience Categories"))* |
| data_value | Decimal(5,2) | Rating associated with the O*NET-SOC occupation |
| n | Decimal(4,0) | Sample size |
| standard_error | Decimal(7,4) | Standard Error |
| lower_ci_bound | Decimal(7,4) | Lower 95% confidence interval bound |
| upper_ci_bound | Decimal(7,4) | Upper 95% confidence interval bound |
| recommend_suppress | Character(1) | Low precision indicator (Y=yes, N=no) |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

This file contains the percent frequency data associated with Education, Training, and Experience Content Model elements. It is displayed in 12 tab delimited fields and identified using the column names provided above. Item rating level metadata is provided in columns named n, standard_error, lower_ci_bound, upper_ci_bound, recommend_suppress, date_updated, and domain_source. Refer to **[Appendix 2, *Item Rating Level Statistics - Incumbent*](appendix_incumbent.html "Appendix 2. Item Rating Level Statistics - Incumbent")** for additional information on these items. The 12 fields are represented by one row. There are a total of 37,125 rows of data in this file.

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 | Added as a new file |
| 5.1 | Columns added for N, Standard Error, Lower CI Bound, Upper CI Bound, and Recommend Suppress |
| 6.0 - 28.1 | No structure changes |
| 28.2 | Standard Error, Lower CI Bound, Upper CI Bound expanded from 2 decimal places to 4 |
| 28.3 - 30.1 | No structure changes |

### Data Example - education_training_experience:

| onetsoc_code | element_id | scale_id | category | data_value | n | standard_error | lower_ci_bound | upper_ci_bound | recommend_suppress | date_updated | domain_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 33-9011.00 | 2.D.1 | RL | 1 | 0.00 | 26 | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 33-9011.00 | 2.D.1 | RL | 2 | 65.38 | 26 | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 33-9011.00 | 2.D.1 | RL | 3 | 19.23 | 26 | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 33-9011.00 | 2.D.1 | RL | 4 | 0.00 | 26 | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 33-9011.00 | 2.D.1 | RL | 5 | 11.54 | 26 | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 33-9011.00 | 2.D.1 | RL | 6 | 3.85 | 26 | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 33-9011.00 | 2.D.1 | RL | 7 | 0.00 | 26 | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 33-9011.00 | 2.D.1 | RL | 8 | 0.00 | 26 | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 33-9011.00 | 2.D.1 | RL | 9 | 0.00 | 26 | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 33-9011.00 | 2.D.1 | RL | 10 | 0.00 | 26 | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 33-9011.00 | 2.D.1 | RL | 11 | 0.00 | 26 | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 33-9011.00 | 2.D.1 | RL | 12 | 0.00 | 26 | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |

---

# emerging_tasks.md

# Emerging Tasks

* [Excel](/dictionary/30.1/excel/emerging_tasks.html)
* [Text](/dictionary/30.1/text/emerging_tasks.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/emerging_tasks.html)
* [Oracle](/dictionary/30.1/oracle/emerging_tasks.html)

| **Purpose:** | Provide emerging task data associated with some O*NET-SOC occupations. |
| **Table Name:** | emerging_tasks |
| **Download:** | [26_emerging_tasks.sql](/dl_files/database/db_30_1_mysql/26_emerging_tasks.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| task | Character Varying(1000) | New or revised task associated with an occupation |
| category | Character Varying(8) | “New” or “Revision” |
| original_task_id | Decimal(8,0) | Task ID referencing original task *(see [*Task Statements*](task_statements.html "Task Statements"))* |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

This file contains new and revised task statements proposed for future data collection. Statements are developed by analysts from sources including feedback from surveyed job incumbents, research into emerging technologies, and information provided by professional associations. The file is displayed in six tab delimited fields with the columns named O*NET-SOC Code, Task, Category, Original Task ID, Date, and Domain Source. The six fields are represented by one row. There are a total of 328 rows of data in this file.

For more information, see:
* [Identification of Emerging Tasks in the O*NET System: A Revised Approach](https://www.onetcenter.org/reports/EmergingTasks_RevisedApproach.html)
* [Adding Drone-Specific Tasks to the O*NET Database: Initial Identification of Emerging Tasks using ChatGPT](https://www.onetcenter.org/reports/Drone_Tasks.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 20.1 | Added as a new file |
| 20.2 - 28.3 | No structure changes |
| 29.0 | Write-in Total column removed |
| 29.1 - 30.1 | No structure changes |

### Data Example - emerging_tasks:

| onetsoc_code | task | category | original_task_id | date_updated | domain_source |
| --- | --- | --- | --- | --- | --- |
| 39-9031.00 | Adjust workout programs and provide variations to address injuries or muscle soreness. | New | NULL | 2025-08-01 | Occupational Expert |
| 29-2011.00 | Conduct blood typing and antibody screening. | New | NULL | 2025-08-01 | Incumbent |

---

# ete_categories.md

# Education, Training, and Experience Categories

* [Excel](/dictionary/30.1/excel/ete_categories.html)
* [Text](/dictionary/30.1/text/ete_categories.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/ete_categories.html)
* [Oracle](/dictionary/30.1/oracle/ete_categories.html)

| **Purpose:** | Provide descriptions of the Education, Training, and Experience percent frequency categories. |
| **Table Name:** | ete_categories |
| **Download:** | [05_ete_categories.sql](/dl_files/database/db_30_1_mysql/05_ete_categories.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| category | Decimal(3,0) | Category value associated with element |
| category_description | Character Varying(1000) | Detail description of category associated with element |

This file contains the categories associated with the Education, Training, and Experience content area. Categories for the following scales are included: Required Level of Education (RL), Related Work Experience (RW), On-Site or In-Plant Training (PT), and On-The-Job Training (OJ). The file is displayed in four tab delimited fields with the columns named Element ID, Scale ID, Category, and Category Description. The four fields are represented by one row. There are a total of 41 rows of data in this file.

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 9.0 | Added as a new file |
| 10.0 - 30.1 | No structure changes |

### Data Example - ete_categories:

| element_id | scale_id | category | category_description |
| --- | --- | --- | --- |
| 3.A.1 | RW | 1 | None |
| 3.A.1 | RW | 2 | Up to and including 1 month |
| 3.A.1 | RW | 3 | Over 1 month, up to and including 3 months |
| 3.A.1 | RW | 4 | Over 3 months, up to and including 6 months |
| 3.A.1 | RW | 5 | Over 6 months, up to and including 1 year |
| 3.A.1 | RW | 6 | Over 1 year, up to and including 2 years |
| 3.A.1 | RW | 7 | Over 2 years, up to and including 4 years |
| 3.A.1 | RW | 8 | Over 4 years, up to and including 6 years |
| 3.A.1 | RW | 9 | Over 6 years, up to and including 8 years |
| 3.A.1 | RW | 10 | Over 8 years, up to and including 10 years |
| 3.A.1 | RW | 11 | Over 10 years |

---

# interests.md

# Interests

* [Excel](/dictionary/30.1/excel/interests.html)
* [Text](/dictionary/30.1/text/interests.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/interests.html)
* [Oracle](/dictionary/30.1/oracle/interests.html)

| **Purpose:** | Provide general occupational interest (RIASEC) high-point codes and numeric profile data for each O*NET-SOC occupation. |
| **Table Name:** | interests |
| **Download:** | [13_interests.sql](/dl_files/database/db_30_1_mysql/13_interests.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| data_value | Decimal(5,2) | Rating associated with the O*NET-SOC occupation |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

This file contains the general occupational interest (RIASEC) high-point codes and numeric profile data for each O*NET-SOC occupation. Interest ratings are presented as two scales: OI reports the RIASEC level of each interest and IH presents “high-point codes”, the numbers of the RIASEC scales for the first, second and/or third highest ratings. The high-point values represent the following elements:

|   | 0.00 = No high point available |   |
|---|---|---|
|   | 1.00 = Realistic |   |
|   | 2.00 = Investigative |   |
|   | 3.00 = Artistic |   |
|   | 4.00 = Social |   |
|   | 5.00 = Enterprising |   |
|   | 6.00 = Conventional |   |

The file is displayed in six tab delimited fields with the columns named O*NET-SOC Code, Element ID, Scale ID, Data Value, Date, and Domain Source. The six fields are represented by one row. There are a total of 8,307 rows of data in this file.

For more information, see:
* [Using Machine Learning to Develop Occupational Interest Profiles and High-Point Codes for the O*NET System](https://www.onetcenter.org/reports/ML_OIPs.html)
* [Career Returns within the O*NET Interest Profiler Tools](https://www.onetcenter.org/reports/IP_Career_Returns.html)
* [Development of an O*NET® Mini Interest Profiler (Mini-IP) for Mobile Devices: Psychometric Characteristics](https://www.onetcenter.org/reports/Mini-IP.html)
* [Examining the Efficacy of Emoji Anchors for the O*NET Interest Profiler Short Form](https://www.onetcenter.org/reports/IP_Emoji.html)
* [O*NET Interest Profiler Short Form Psychometric Characteristics: Summary](https://www.onetcenter.org/reports/IPSF_Psychometric.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 | Date and Source columns added |
| 5.1 - 30.1 | No structure changes |

### Data Example - interests:

| onetsoc_code | element_id | scale_id | data_value | date_updated | domain_source |
| --- | --- | --- | --- | --- | --- |
| 43-4041.00 | 1.B.1.a | OI | 1.00 | 2023-11-01 | Machine Learning |
| 43-4041.00 | 1.B.1.b | OI | 1.85 | 2023-11-01 | Machine Learning |
| 43-4041.00 | 1.B.1.c | OI | 1.00 | 2023-11-01 | Machine Learning |
| 43-4041.00 | 1.B.1.d | OI | 3.39 | 2023-11-01 | Machine Learning |
| 43-4041.00 | 1.B.1.e | OI | 4.47 | 2023-11-01 | Machine Learning |
| 43-4041.00 | 1.B.1.f | OI | 7.00 | 2023-11-01 | Machine Learning |
| 43-4041.00 | 1.B.1.g | IH | 6.00 | 2023-11-01 | Machine Learning |
| 43-4041.00 | 1.B.1.h | IH | 5.00 | 2023-11-01 | Machine Learning |
| 43-4041.00 | 1.B.1.i | IH | 4.00 | 2023-11-01 | Machine Learning |
| 29-2034.00 | 1.B.1.a | OI | 6.25 | 2023-11-01 | Machine Learning |
| 29-2034.00 | 1.B.1.b | OI | 4.63 | 2023-11-01 | Machine Learning |
| 29-2034.00 | 1.B.1.c | OI | 1.00 | 2023-11-01 | Machine Learning |
| 29-2034.00 | 1.B.1.d | OI | 3.58 | 2023-11-01 | Machine Learning |
| 29-2034.00 | 1.B.1.e | OI | 1.00 | 2023-11-01 | Machine Learning |
| 29-2034.00 | 1.B.1.f | OI | 4.87 | 2023-11-01 | Machine Learning |
| 29-2034.00 | 1.B.1.g | IH | 1.00 | 2023-11-01 | Machine Learning |
| 29-2034.00 | 1.B.1.h | IH | 6.00 | 2023-11-01 | Machine Learning |
| 29-2034.00 | 1.B.1.i | IH | 2.00 | 2023-11-01 | Machine Learning |

---

# interests_illus_activities.md

# Interests Illustrative Activities

* [Excel](/dictionary/30.1/excel/interests_illus_activities.html)
* [Text](/dictionary/30.1/text/interests_illus_activities.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/interests_illus_activities.html)
* [Oracle](/dictionary/30.1/oracle/interests_illus_activities.html)

| **Purpose:** | Provide illustrative work activities related to the general and basic occupational interests. |
| **Table Name:** | interests_illus_activities |
| **Download:** | [39_interests_illus_activities.sql](/dl_files/database/db_30_1_mysql/39_interests_illus_activities.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| interest_type | Character Varying(20) | “General” or “Basic” |
| activity | Character Varying(150) | Illustrative work activity |

This file contains illustrative work activities related to the general and basic occupational interests. The file is displayed in three tab delimited fields with the columns named Element ID, Interest Type, and Activity. The three fields are represented by one row. There are a total of 188 rows of data in this file.

For more information, see:
* [Updating Vocational Interests Information for the O*NET Content Model](https://www.onetcenter.org/reports/Voc_Interests.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 27.2 | Added as a new file |
| 27.3 - 30.1 | No structure changes |

### Data Example - interests_illus_activities:

| element_id | interest_type | activity |
| --- | --- | --- |
| 1.B.1.a | General | Build kitchen cabinets. |
| 1.B.1.a | General | Drive a truck to deliver packages to offices and homes. |
| 1.B.1.a | General | Put out forest fires. |
| 1.B.1.a | General | Repair household appliances. |
| 1.B.1.b | General | Develop a new medicine. |

---

# interests_illus_occupations.md

# Interests Illustrative Occupations

* [Excel](/dictionary/30.1/excel/interests_illus_occupations.html)
* [Text](/dictionary/30.1/text/interests_illus_occupations.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/interests_illus_occupations.html)
* [Oracle](/dictionary/30.1/oracle/interests_illus_occupations.html)

| **Purpose:** | Provide illustrative occupations linked to the general and basic occupational interests. |
| **Table Name:** | interests_illus_occupations |
| **Download:** | [40_interests_illus_occupations.sql](/dl_files/database/db_30_1_mysql/40_interests_illus_occupations.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| interest_type | Character Varying(20) | “General” or “Basic” |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |

This file contains illustrative occupations linked to the general and basic occupational interests. For occupation-specific ratings for RIASEC elements, see the Interests file.

The file is displayed in three tab delimited fields with the columns named Element ID, Interest Type, and O*NET-SOC Code. The three fields are represented by one row. There are a total of 186 rows of data in this file.

For more information, see:
* [Updating Vocational Interests Information for the O*NET Content Model](https://www.onetcenter.org/reports/Voc_Interests.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 27.2 | Added as a new file |
| 27.3 - 30.1 | No structure changes |

### Data Example - interests_illus_occupations:

| element_id | interest_type | onetsoc_code |
| --- | --- | --- |
| 1.B.1.a | General | 17-3024.01 |
| 1.B.1.a | General | 45-2091.00 |
| 1.B.1.a | General | 47-2031.00 |
| 1.B.1.a | General | 53-3052.00 |
| 1.B.1.b | General | 19-1029.04 |

---

# iwa_reference.md

# IWA Reference

* [Excel](/dictionary/30.1/excel/iwa_reference.html)
* [Text](/dictionary/30.1/text/iwa_reference.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/iwa_reference.html)
* [Oracle](/dictionary/30.1/oracle/iwa_reference.html)

| **Purpose:** | Provide each Intermediate Work Activity. |
| **Table Name:** | iwa_reference |
| **Download:** | [23_iwa_reference.sql](/dl_files/database/db_30_1_mysql/23_iwa_reference.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| iwa_id | Character Varying(20) | Identifies each Intermediate Work Activity |
| iwa_title | Character Varying(150) | Intermediate Work Activity statement |

This file contains each Intermediate Work Activity and its corresponding O*NET Work Activity element ID. Every IWA is linked to exactly one Work Activity from the O*NET Content Model. IWAs are linked to one or more DWAs; see the [*DWA Reference*](dwa_reference.html "DWA Reference") file for these links.

The file is displayed in three tab delimited fields with the columns named Element ID, IWA ID, and IWA Title. The three fields are represented by one row. There are a total of 332 rows of data in this file.

For more information, see:
* [O*NET Work Activities Project Technical Report](https://www.onetcenter.org/reports/DWA_2014.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 18.1 | Added as a new file |
| 19.0 - 30.1 | No structure changes |

### Data Example - iwa_reference:

| element_id | iwa_id | iwa_title |
| --- | --- | --- |
| 4.A.1.a.1 | 4.A.1.a.1.I01 | Study details of artistic productions. |
| 4.A.1.a.1 | 4.A.1.a.1.I02 | Read documents or materials to inform work processes. |
| 4.A.2.b.2 | 4.A.2.b.2.I14 | Design industrial systems or equipment. |
| 4.A.4.c.2 | 4.A.4.c.2.I01 | Perform recruiting or hiring activities. |

---

# job_zone_reference.md

# Job Zone Reference

* [Excel](/dictionary/30.1/excel/job_zone_reference.html)
* [Text](/dictionary/30.1/text/job_zone_reference.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/job_zone_reference.html)
* [Oracle](/dictionary/30.1/oracle/job_zone_reference.html)

| **Purpose:** | Provide Job Zone data (developed to help transition DOT’s measures of Specific Vocational Preparation (SVP) to O*NET’s measure of experience, education, and job training). |
| **Table Name:** | job_zone_reference |
| **Download:** | [02_job_zone_reference.sql](/dl_files/database/db_30_1_mysql/02_job_zone_reference.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| job_zone | Decimal(1,0) | Job Zone number |
| name | Character Varying(50) | Job Zone name/zone |
| experience | Character Varying(300) | Job Zone experience requirements |
| education | Character Varying(500) | Job Zone educational requirements |
| job_training | Character Varying(300) | Job Zone training requirements |
| examples | Character Varying(500) | Job Zone examples |
| svp_range | Character Varying(25) | Specific vocational preparation range |

This file describes the five O*NET Job Zones, which are groups of occupations that need the same level of experience, education, and training. The file is displayed in seven tab delimited fields with the columns named Job Zone, Name, Experience, Education, Job Training, Examples, and SVP Range. The seven fields are represented by one row. There are a total of 5 rows of data in this file.

For more information, see:
* [Procedures for O*NET Job Zone Assignment](https://www.onetcenter.org/reports/JobZoneProcedure.html)
* [Procedures for O*NET Job Zone Assignment: Updated to Include Procedures for Developing Preliminary Job Zones for New O*NET-SOC Occupations](https://www.onetcenter.org/reports/JobZoneProcedureUpdate.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 - 30.1 | No structure changes |

### Data Example - job_zone_reference:

| job_zone | name | experience | education | job_training | examples | svp_range |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Job Zone One: Little or No Preparation Needed | Little or no previous work-related skill, knowledge, or experience is needed for these occupations. For example, a person can become a waiter or waitress even if he/she has never worked before. | Some of these occupations may require a high school diploma or GED certificate. | Employees in these occupations need anywhere from a few days to a few months of training. Usually, an experienced worker could show you how to do the job. | These occupations involve following instructions and helping others. Examples include agricultural equipment operators, dishwashers, floor sanders and finishers, landscaping and groundskeeping workers, logging equipment operators, baristas, and maids and housekeeping cleaners. | (Below 4.0) |
| 2 | Job Zone Two: Some Preparation Needed | Some previous work-related skill, knowledge, or experience is usually needed. For example, a teller would benefit from experience working directly with the public. | These occupations usually require a high school diploma. | Employees in these occupations need anywhere from a few months to one year of working with experienced employees. A recognized apprenticeship program may be associated with these occupations. | These occupations often involve using your knowledge and skills to help others. Examples include orderlies, counter and rental clerks, customer service representatives, security guards, upholsterers, tellers, and dental laboratory technicians. | (4.0 to < 6.0) |
| 3 | Job Zone Three: Medium Preparation Needed | Previous work-related skill, knowledge, or experience is required for these occupations. For example, an electrician must have completed three or four years of apprenticeship or several years of vocational training, and often must have passed a licensing exam, in order to perform the job. | Most occupations in this zone require training in vocational schools, related on-the-job experience, or an associate's degree. | Employees in these occupations usually need one or two years of training involving both on-the-job experience and informal training with experienced workers. A recognized apprenticeship program may be associated with these occupations. | These occupations usually involve using communication and organizational skills to coordinate, supervise, manage, or train others to accomplish goals. Examples include hydroelectric production managers, desktop publishers, electricians, agricultural technicians, barbers, court reporters and simultaneous captioners, and medical assistants. | (6.0 to < 7.0) |

---

# job_zones.md

# Job Zones

* [Excel](/dictionary/30.1/excel/job_zones.html)
* [Text](/dictionary/30.1/text/job_zones.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/job_zones.html)
* [Oracle](/dictionary/30.1/oracle/job_zones.html)

| **Purpose:** | Provide a mapping of O*NET-SOC occupations to Job Zone ratings. |
| **Table Name:** | job_zones |
| **Download:** | [14_job_zones.sql](/dl_files/database/db_30_1_mysql/14_job_zones.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| job_zone | Decimal(1,0) | Job Zone number *(see [*Job Zone Reference*](job_zone_reference.html "Job Zone Reference"))* |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

This file contains each O*NET-SOC code and its corresponding Job Zone number. The file is displayed in four tab delimited fields with the columns named O*NET-SOC Code, Job Zone, Date, and Domain Source. The four fields are represented by one row. There are a total of 923 rows of data in this file.

For more information, see:
* [Procedures for O*NET Job Zone Assignment](https://www.onetcenter.org/reports/JobZoneProcedure.html)
* [Procedures for O*NET Job Zone Assignment: Updated to Include Procedures for Developing Preliminary Job Zones for New O*NET-SOC Occupations](https://www.onetcenter.org/reports/JobZoneProcedureUpdate.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 | No structure changes |
| 5.1 | Date and Domain Source columns added |
| 6.0 - 30.1 | No structure changes |

### Data Example - job_zones:

| onetsoc_code | job_zone | date_updated | domain_source |
| --- | --- | --- | --- |
| 17-3026.01 | 4 | 2025-08-01 | Analyst |
| 27-4014.00 | 3 | 2025-08-01 | Analyst |
| 13-1199.04 | 4 | 2025-08-01 | Analyst |
| 49-3011.00 | 3 | 2025-08-01 | Analyst |
| 45-3031.00 | 1 | 2025-08-01 | Analyst |
| 39-6012.00 | 2 | 2025-08-01 | Analyst |

---

# knowledge.md

# Knowledge

* [Excel](/dictionary/30.1/excel/knowledge.html)
* [Text](/dictionary/30.1/text/knowledge.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/knowledge.html)
* [Oracle](/dictionary/30.1/oracle/knowledge.html)

| **Purpose:** | Provide a mapping of O*NET-SOC codes (occupations) to Knowledge ratings. |
| **Table Name:** | knowledge |
| **Download:** | [15_knowledge.sql](/dl_files/database/db_30_1_mysql/15_knowledge.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| data_value | Decimal(5,2) | Rating associated with the O*NET-SOC occupation |
| n | Decimal(4,0) | Sample size |
| standard_error | Decimal(7,4) | Standard Error |
| lower_ci_bound | Decimal(7,4) | Lower 95% confidence interval bound |
| upper_ci_bound | Decimal(7,4) | Upper 95% confidence interval bound |
| recommend_suppress | Character(1) | Low precision indicator (Y=yes, N=no) |
| not_relevant | Character(1) | Not relevant for the occupation (Y=yes, N=no) |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

This file contains the Content Model Knowledge data associated with each O*NET-SOC occupation. It is displayed in 12 tab delimited fields and identified using the column names provided above. Item rating level metadata is provided in columns named n, standard_error, lower_ci_bound, upper_ci_bound, recommend_suppress, not_relevant, date_updated, and domain_source. Refer to **[Appendix 2, *Item Rating Level Statistics - Incumbent*](appendix_incumbent.html "Appendix 2. Item Rating Level Statistics - Incumbent")** for additional information on these items. The 12 fields are represented by one row. There are a total of 59,004 rows of data in this file.

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 | Date and Source columns added |
| 5.1 | Columns added for N, Standard Error, Lower CI Bound, Upper CI Bound, Recommend Suppress, and Not Relevant |
| 6.0 - 28.1 | No structure changes |
| 28.2 | Standard Error, Lower CI Bound, Upper CI Bound expanded from 2 decimal places to 4 |
| 28.3 - 30.1 | No structure changes |

### Data Example - knowledge:

| onetsoc_code | element_id | scale_id | data_value | n | standard_error | lower_ci_bound | upper_ci_bound | recommend_suppress | not_relevant | date_updated | domain_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 29-2011.00 | 2.C.8.b | IM | 2.52 | 28 | 0.2879 | 1.9275 | 3.1090 | N | NULL | 2025-08-01 | Incumbent |
| 29-2011.00 | 2.C.8.b | LV | 2.47 | 28 | 0.4408 | 1.5705 | 3.3792 | N | N | 2025-08-01 | Incumbent |
| 29-2011.00 | 2.C.9.a | IM | 2.30 | 28 | 0.1504 | 1.9912 | 2.6086 | N | NULL | 2025-08-01 | Incumbent |
| 29-2011.00 | 2.C.9.a | LV | 1.64 | 28 | 0.3761 | 0.8672 | 2.4105 | N | N | 2025-08-01 | Incumbent |
| 29-2011.00 | 2.C.9.b | IM | 1.80 | 28 | 0.2181 | 1.3530 | 2.2482 | N | NULL | 2025-08-01 | Incumbent |
| 29-2011.00 | 2.C.9.b | LV | 1.46 | 28 | 0.4430 | 0.5467 | 2.3648 | N | N | 2025-08-01 | Incumbent |
| 29-2011.00 | 2.C.10 | IM | 1.75 | 27 | 0.1723 | 1.3918 | 2.1002 | N | NULL | 2025-08-01 | Incumbent |
| 29-2011.00 | 2.C.10 | LV | 1.28 | 27 | 0.2805 | 0.7064 | 1.8596 | N | N | 2025-08-01 | Incumbent |

---

# level_scale_anchors.md

# Level Scale Anchors

* [Excel](/dictionary/30.1/excel/level_scale_anchors.html)
* [Text](/dictionary/30.1/text/level_scale_anchors.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/level_scale_anchors.html)
* [Oracle](/dictionary/30.1/oracle/level_scale_anchors.html)

| **Purpose:** | Provide descriptions of O*NET Level Scale Anchors. |
| **Table Name:** | level_scale_anchors |
| **Download:** | [06_level_scale_anchors.sql](/dl_files/database/db_30_1_mysql/06_level_scale_anchors.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| anchor_value | Decimal(3,0) | Anchor value associated with element |
| anchor_description | Character Varying(1000) | Detail description of anchor associated with element |

This file contains the scale anchors associated with the following four content areas – 1) Abilities, 2) Knowledge, 3) Skills, and 4) Work Activities. It includes all scale anchors utilized in the data collection survey where the scale anchors are variable and item specific. Scale anchors are not included for those survey items where the scale anchors are fixed. This includes the five-point importance scale and the seven-point task frequency scale. (Note: See [O*NET Data Questionnaires](https://www.onetcenter.org/ombclearance.html)).

The file is displayed in four tab delimited fields with the columns named Element ID, Scale ID, Anchor Value, and Anchor Description. The four fields are represented by one row. There are a total of 483 rows of data in this file.

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.1 | Added as a new file |
| 6.0 | Added Scale ID column |
| 7.0 - 8.0 | No structure changes |
| 9.0 | The data for Education, Training, and Experience and Work Context were moved into their own files for data clarity purposes. |
| 10.0 - 30.1 | No structure changes |

### Data Example - level_scale_anchors:

| element_id | scale_id | anchor_value | anchor_description |
| --- | --- | --- | --- |
| 1.A.1.a.1 | LV | 2 | Understand a television commercial |
| 1.A.1.a.1 | LV | 4 | Understand a coach's oral instructions for a sport |
| 1.A.1.a.1 | LV | 6 | Understand a lecture on advanced physics |
| 1.A.1.a.2 | LV | 2 | Understand signs on the highway |
| 1.A.1.a.2 | LV | 4 | Understand an apartment lease |
| 1.A.1.a.2 | LV | 6 | Understand an instruction book on repairing Artificial Intelligence systems |
| 1.A.1.a.3 | LV | 2 | Place an order at a restaurant drive-thru |
| 1.A.1.a.3 | LV | 4 | Give instructions to a lost motorist |
| 1.A.1.a.3 | LV | 6 | Explain advanced principles of genetics to college freshmen |
| 1.A.1.a.4 | LV | 1 | Write a note to remind someone to take food out of the freezer |
| 1.A.1.a.4 | LV | 4 | Write a job recommendation for a subordinate |

---

# occupation_data.md

# Occupation Data

* [Excel](/dictionary/30.1/excel/occupation_data.html)
* [Text](/dictionary/30.1/text/occupation_data.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/occupation_data.html)
* [Oracle](/dictionary/30.1/oracle/occupation_data.html)

| **Purpose:** | Provide O*NET-SOC codes, titles, and descriptions. |
| **Table Name:** | occupation_data |
| **Download:** | [03_occupation_data.sql](/dl_files/database/db_30_1_mysql/03_occupation_data.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code |
| title | Character Varying(150) | O*NET-SOC Title |
| description | Character Varying(1000) | O*NET-SOC Description |

This file contains each O*NET-SOC code, occupational title, and definition/description. The file is displayed in three tab delimited fields with the columns named O*NET-SOC Code, Title, and Description. The three fields are represented by one row. There are a total of 1,016 rows of data in this file.

For more information, see:
* [Updating the O*NET-SOC Taxonomy: Incorporating the 2010 SOC Structure](https://www.onetcenter.org/reports/Taxonomy2010.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 - 30.1 | No structure changes |

### Data Example - occupation_data:

| onetsoc_code | title | description |
| --- | --- | --- |
| 11-9041.01 | Biofuels/Biodiesel Technology and Product Development Managers | Define, plan, or execute biofuels/biodiesel research programs that evaluate alternative feedstock and process technologies with near-term commercial potential. |
| 17-2072.00 | Electronics Engineers, Except Computer | Research, design, develop, or test electronic components and systems for commercial, industrial, military, or scientific use employing knowledge of electronic theory and materials properties. Design electronic circuits and components for use in fields such as telecommunications, aerospace guidance and propulsion control, acoustics, or instruments and controls. |
| 19-4031.00 | Chemical Technicians | Conduct chemical and physical laboratory tests to assist scientists in making qualitative and quantitative analyses of solids, liquids, and gaseous materials for research and development of new products or processes, quality control, maintenance of environmental standards, and other work involving experimental, theoretical, or practical application of chemistry and related sciences. |
| 45-4011.00 | Forest and Conservation Workers | Under supervision, perform manual labor necessary to develop, maintain, or protect areas such as forests, forested areas, woodlands, wetlands, and rangelands through such activities as raising and transporting seedlings; combating insects, pests, and diseases harmful to plant life; and building structures to control water, erosion, and leaching of soil. Includes forester aides, seedling pullers, tree planters, and gatherers of nontimber forestry products such as pine straw. |
| 51-8012.00 | Power Distributors and Dispatchers | Coordinate, regulate, or distribute electricity or steam. |

---

# occupation_level_metadata.md

# Occupation Level Metadata

* [Excel](/dictionary/30.1/excel/occupation_level_metadata.html)
* [Text](/dictionary/30.1/text/occupation_level_metadata.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/occupation_level_metadata.html)
* [Oracle](/dictionary/30.1/oracle/occupation_level_metadata.html)

| **Purpose:** | Provide O*NET-SOC Occupational Level Metadata associated with the incumbent data collection. |
| **Table Name:** | occupation_level_metadata |
| **Download:** | [07_occupation_level_metadata.sql](/dl_files/database/db_30_1_mysql/07_occupation_level_metadata.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| item | Character Varying(150) | Occupation level statistics |
| response | Character Varying(75) | Type of response |
| n | Decimal(4,0) | Sample size for occupation |
| percent | Decimal(4,1) | Percentage of responses |
| date_updated | Date | Date when data was updated |

This file contains occupational level metadata variables associated with data collection statistics. Refer to **[Appendix 3, *Key to Occupation Level Metadata*](appendix_metadata.html "Appendix 3. Key to Occupation Level Metadata")** for additional descriptions of the data provided in this file.

The file is displayed in six tab delimited fields with the columns named O*NET-SOC Code, Item, Response, N, Percent, and Date. The six fields are represented by one row. There are a total of 32,202 rows of data in this file.

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.1 | Added as a new file |
| 6.0 - 20.3 | No structure changes |
| 21.0 | Items added and renamed; see [Appendix 3, *Key to Occupation Level Metadata*](appendix_metadata.html "Appendix 3. Key to Occupation Level Metadata") |
| 21.1 - 30.1 | No structure changes |

### Data Example - occupation_level_metadata:

| onetsoc_code | item | response | n | percent | date_updated |
| --- | --- | --- | --- | --- | --- |
| 17-2111.02 | Data Collection Mode | Paper | 26 | 15.4 | 2025-08-01 |
| 17-2111.02 | Data Collection Mode | Web | 26 | 84.6 | 2025-08-01 |
| 17-2111.02 | How Much Experience Performing Work in this Occupation | 1-2 Years | 26 | 0.0 | 2025-08-01 |
| 17-2111.02 | How Much Experience Performing Work in this Occupation | 10+ Years | 26 | 96.2 | 2025-08-01 |
| 17-2111.02 | How Much Experience Performing Work in this Occupation | 3-4 Years | 26 | 0.0 | 2025-08-01 |
| 17-2111.02 | How Much Experience Performing Work in this Occupation | 5-9 Years | 26 | 3.8 | 2025-08-01 |
| 17-2111.02 | How Much Experience Performing Work in this Occupation | <1 Year | 26 | 0.0 | 2025-08-01 |
| 17-2111.02 | How Much Experience Performing Work in this Occupation | Missing | 26 | 0.0 | 2025-08-01 |
| 17-2111.02 | How Much Experience Performing Work in this Occupation | Never performed work in the occupation | 26 | 0.0 | 2025-08-01 |
| 17-2111.02 | OE Completeness Rate | NULL | NULL | 100.0 | 2025-08-01 |
| 17-2111.02 | OE Response Rate | NULL | NULL | 50.0 | 2025-08-01 |
| 17-2111.02 | Total Completed Questionnaires | NULL | 26 | NULL | 2025-08-01 |
| 17-2112.00 | Data Collection Mode | Paper | 84 | 42.9 | 2020-08-01 |
| 17-2112.00 | Data Collection Mode | Web | 84 | 57.1 | 2020-08-01 |
| 17-2112.00 | Employee Completeness Rate | NULL | NULL | 90.3 | 2020-08-01 |
| 17-2112.00 | Employee Response Rate | NULL | NULL | 68.4 | 2020-08-01 |

---

# related_occupations.md

# Related Occupations

* [Excel](/dictionary/30.1/excel/related_occupations.html)
* [Text](/dictionary/30.1/text/related_occupations.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/related_occupations.html)
* [Oracle](/dictionary/30.1/oracle/related_occupations.html)

| **Purpose:** | Provide related occupation links between O*NET-SOC occupations. |
| **Table Name:** | related_occupations |
| **Download:** | [27_related_occupations.sql](/dl_files/database/db_30_1_mysql/27_related_occupations.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| related_onetsoc_code | Character(10) | Related O*NET-SOC code mapping *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| relatedness_tier | Character Varying(50) | Categories indicating level of relatedness |
| related_index | Decimal(3,0) | Order of related code mappings based on expert review |

For each O*NET-SOC code included, 10 primary and 10 supplemental related O*NET-SOC codes are listed. The related occupations in this file are developed using an approach which includes three important contributors to occupational similarity: what people in the occupations do, what they know, and what they are called. The “Relatedness Tier” column assigns one of three categories to each link:
* **Primary-Short** — Five most strongly related occupations after expert review.
* **Primary-Long** — 6th to 10th most strongly related occupations after expert review.
* **Supplemental** — 11th to 20th most strongly related occupations after expert review.

The file is displayed in four tab delimited fields with the columns named O*NET-SOC Code, Related O*NET-SOC Code, Relatedness Tier, and Index. The four fields are represented by one row. There are a total of 18,460 rows of data in this file.

For more information, see:
* [Developing Related Occupations for the O*NET Program](https://www.onetcenter.org/reports/Related_2022.html)
* [Updates to Related Occupations for the O*NET Program Using the O*NET 28.0 Database](https://www.onetcenter.org/reports/Related_2024.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 26.3 | Added as a new file |
| 27.0 - 30.1 | No structure changes |

### Data Example - related_occupations:

| onetsoc_code | related_onetsoc_code | relatedness_tier | related_index |
| --- | --- | --- | --- |
| 17-1011.00 | 17-1012.00 | Primary-Short | 1 |
| 17-1011.00 | 11-9021.00 | Primary-Short | 2 |
| 17-1011.00 | 27-1025.00 | Primary-Short | 3 |
| 17-1011.00 | 17-2051.00 | Primary-Short | 4 |
| 17-1011.00 | 47-4011.00 | Primary-Short | 5 |
| 17-1011.00 | 11-9041.00 | Primary-Long | 6 |
| 17-1011.00 | 17-2112.00 | Primary-Long | 7 |

---

# riasec_keywords.md

# RIASEC Keywords

* [Excel](/dictionary/30.1/excel/riasec_keywords.html)
* [Text](/dictionary/30.1/text/riasec_keywords.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/riasec_keywords.html)
* [Oracle](/dictionary/30.1/oracle/riasec_keywords.html)

| **Purpose:** | Provide action and object keywords for each general occupational interest. |
| **Table Name:** | riasec_keywords |
| **Download:** | [37_riasec_keywords.sql](/dl_files/database/db_30_1_mysql/37_riasec_keywords.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| keyword | Character Varying(150) | Relevant interest keyword |
| keyword_type | Character Varying(20) | “Action” or “Object” |

This file contains action and object keywords for each general occupational interest. The file is displayed in three tab delimited fields with the columns named Element ID, Keyword, and Keyword Type. The three fields are represented by one row. There are a total of 75 rows of data in this file.

For more information, see:
* [Updating Vocational Interests Information for the O*NET Content Model](https://www.onetcenter.org/reports/Voc_Interests.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 27.2 | Added as a new file |
| 27.3 - 30.1 | No structure changes |

### Data Example - riasec_keywords:

| element_id | keyword | keyword_type |
| --- | --- | --- |
| 1.B.1.a | Build | Action |
| 1.B.1.a | Drive | Action |
| 1.B.1.a | Install | Action |
| 1.B.1.a | Maintain | Action |
| 1.B.1.a | Repair | Action |

---

# sample_of_reported_titles.md

# Sample of Reported Titles

* [Excel](/dictionary/30.1/excel/sample_of_reported_titles.html)
* [Text](/dictionary/30.1/text/sample_of_reported_titles.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/sample_of_reported_titles.html)
* [Oracle](/dictionary/30.1/oracle/sample_of_reported_titles.html)

| **Purpose:** | Provide job titles reported during O*NET data collection. |
| **Table Name:** | sample_of_reported_titles |
| **Download:** | [30_sample_of_reported_titles.sql](/dl_files/database/db_30_1_mysql/30_sample_of_reported_titles.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| reported_job_title | Character Varying(150) | Title from incumbents or occupational experts |
| shown_in_my_next_move | Character(1) | Whether title is shown on My Next Move career page (Y=yes, N=no) |

This file contains job titles frequently reported by incumbents and occupational experts on data collection surveys. These titles are displayed on occupational reports in the O*NET OnLine and O*NET Code Connector web applications; up to 10 titles for each occupation are displayed and included in this file. Up to 4 titles are also displayed in My Next Move, My Next Move for Veterans, and Mi Próximo Paso; the titles shown in these applications are marked with a Y in the “Shown in My Next Move” column.

The file is displayed in three tab delimited fields with the columns named O*NET-SOC Code, Reported Job Title, and Shown in My Next Move. The three fields are represented by one row. There are a total of 7,955 rows of data in this file.

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 20.1 | Added as a new file |
| 20.2 - 30.1 | No structure changes |

### Data Example - sample_of_reported_titles:

| onetsoc_code | reported_job_title | shown_in_my_next_move |
| --- | --- | --- |
| 17-2071.00 | Circuits Engineer | N |
| 17-2071.00 | Design Engineer | Y |
| 17-2071.00 | Electrical Controls Engineer | N |
| 17-2071.00 | Electrical Design Engineer | Y |
| 17-2071.00 | Electrical Engineer | Y |
| 17-2071.00 | Electrical Project Engineer | N |
| 17-2071.00 | Engineer | N |
| 17-2071.00 | Instrumentation and Electrical Reliability Engineer (I&E Reliability Engineer) | N |

---

# scales_reference.md

# Scales Reference

* [Excel](/dictionary/30.1/excel/scales_reference.html)
* [Text](/dictionary/30.1/text/scales_reference.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/scales_reference.html)
* [Oracle](/dictionary/30.1/oracle/scales_reference.html)

| **Purpose:** | Provide a reference to the scale names and values. |
| **Table Name:** | scales_reference |
| **Download:** | [04_scales_reference.sql](/dl_files/database/db_30_1_mysql/04_scales_reference.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| scale_id | Character Varying(3) | Scale ID |
| scale_name | Character Varying(50) | Scale Name |
| minimum | Decimal(1,0) | Scale Minimum |
| maximum | Decimal(3,0) | Scale Maximum |

This file contains the Scale information by which the raw values are measured. The file is displayed in four tab delimited fields with the columns named Scale ID, Scale Name, Minimum, and Maximum. The four fields are represented by one row. There are a total of 31 rows of data in this file.

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 - 30.1 | No structure changes |

### Data Example - scales_reference:

| scale_id | scale_name | minimum | maximum |
| --- | --- | --- | --- |
| CT | Context | 1 | 3 |
| CTP | Context (Categories 1-3) | 0 | 100 |
| CX | Context | 1 | 5 |
| CXP | Context (Categories 1-5) | 0 | 100 |
| IM | Importance | 1 | 5 |
| LV | Level | 0 | 7 |
| OJ | On-The-Job Training (Categories 1-9) | 0 | 100 |
| PT | On-Site Or In-Plant Training (Categories 1-9) | 0 | 100 |
| RL | Required Level Of Education (Categories 1-12) | 0 | 100 |
| RW | Related Work Experience (Categories 1-11) | 0 | 100 |

---

# skills.md

# Skills

* [Excel](/dictionary/30.1/excel/skills.html)
* [Text](/dictionary/30.1/text/skills.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/skills.html)
* [Oracle](/dictionary/30.1/oracle/skills.html)

| **Purpose:** | Provide a mapping of O*NET-SOC codes (occupations) to Skill ratings. |
| **Table Name:** | skills |
| **Download:** | [16_skills.sql](/dl_files/database/db_30_1_mysql/16_skills.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| data_value | Decimal(5,2) | Rating associated with the O*NET-SOC occupation |
| n | Decimal(4,0) | Sample size |
| standard_error | Decimal(7,4) | Standard Error |
| lower_ci_bound | Decimal(7,4) | Lower 95% confidence interval bound |
| upper_ci_bound | Decimal(7,4) | Upper 95% confidence interval bound |
| recommend_suppress | Character(1) | Low precision indicator (Y=yes, N=no) |
| not_relevant | Character(1) | Not relevant for the occupation (Y=yes, N=no) |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

This file contains the Content Model Skill data associated with each O*NET-SOC occupation. It is displayed in 12 tab delimited fields and identified using the column names provided above. Item rating level metadata is provided in columns named n, standard_error, lower_ci_bound, upper_ci_bound, recommend_suppress, not_relevant, date_updated, and domain_source. Refer to **[Appendix 1, *Item Rating Level Statistics - Analyst*](appendix_analyst.html "Appendix 1. Item Rating Level Statistics - Analyst")** for additional information on these items. The 12 fields are represented by one row. There are a total of 62,580 rows of data in this file.

For more information, see:
* [O*NET Analyst Occupational Skills Ratings: Procedures Update](https://www.onetcenter.org/reports/AOSkills_ProcUpdate.html)

### Data Example - skills:

| onetsoc_code | element_id | scale_id | data_value | n | standard_error | lower_ci_bound | upper_ci_bound | recommend_suppress | not_relevant | date_updated | domain_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 49-3041.00 | 2.A.1.a | IM | 3.00 | 8 | 0.0000 | 3.0000 | 3.0000 | N | NULL | 2025-08-01 | Analyst |
| 49-3041.00 | 2.A.1.a | LV | 2.88 | 8 | 0.1250 | 2.6300 | 3.1200 | N | N | 2025-08-01 | Analyst |
| 49-3041.00 | 2.A.1.b | IM | 3.12 | 8 | 0.1250 | 2.8800 | 3.3700 | N | NULL | 2025-08-01 | Analyst |
| 49-3041.00 | 2.A.1.b | LV | 3.00 | 8 | 0.0000 | 3.0000 | 3.0000 | N | N | 2025-08-01 | Analyst |
| 49-3041.00 | 2.A.1.c | IM | 2.88 | 8 | 0.1250 | 2.6300 | 3.1200 | N | NULL | 2025-08-01 | Analyst |
| 49-3041.00 | 2.A.1.c | LV | 2.62 | 8 | 0.1830 | 2.2664 | 2.9836 | N | N | 2025-08-01 | Analyst |
| 49-3041.00 | 2.A.1.d | IM | 3.12 | 8 | 0.1250 | 2.8800 | 3.3700 | N | NULL | 2025-08-01 | Analyst |
| 49-3041.00 | 2.A.1.d | LV | 3.00 | 8 | 0.0000 | 3.0000 | 3.0000 | N | N | 2025-08-01 | Analyst |

---

# skills_to_work_activities.md

# Skills to Work Activities

* [Excel](/dictionary/30.1/excel/skills_to_work_activities.html)
* [Text](/dictionary/30.1/text/skills_to_work_activities.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/skills_to_work_activities.html)
* [Oracle](/dictionary/30.1/oracle/skills_to_work_activities.html)

| **Purpose:** | Provide linkages between skills and relevant work activities. |
| **Table Name:** | skills_to_work_activities |
| **Download:** | [35_skills_to_work_activities.sql](/dl_files/database/db_30_1_mysql/35_skills_to_work_activities.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| skills_element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| work_activities_element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |

This file contains linkages between skills and relevant work activities. Occupation-specific ratings for the listed elements may be found in the [*Skills*](skills.html "Skills") and [*Work Activities*](work_activities.html "Work Activities") files. Linkages were developed by a panel of experienced industrial/organizational psychologists, and are used in the development of analyst occupational skills ratings.

The file is displayed in two tab delimited fields with the columns named Skills Element ID and Work Activities Element ID. The two fields are represented by one row. There are a total of 232 rows of data in this file.

For more information, see:
* [O*NET Analyst Occupational Skills Ratings: Procedures Update](https://www.onetcenter.org/reports/AOSkills_ProcUpdate.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 24.2 | Added as a new file |
| 24.3 - 30.1 | No structure changes |

### Data Example - skills_to_work_activities:

| skills_element_id | work_activities_element_id |
| --- | --- |
| 2.A.1.a | 4.A.1.a.1 |
| 2.A.1.a | 4.A.1.a.2 |
| 2.A.1.a | 4.A.1.b.1 |
| 2.A.1.a | 4.A.2.a.1 |
| 2.A.1.a | 4.A.2.a.2 |

---

# skills_to_work_context.md

# Skills to Work Context

* [Excel](/dictionary/30.1/excel/skills_to_work_context.html)
* [Text](/dictionary/30.1/text/skills_to_work_context.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/skills_to_work_context.html)
* [Oracle](/dictionary/30.1/oracle/skills_to_work_context.html)

| **Purpose:** | Provide linkages between skills and relevant work context. |
| **Table Name:** | skills_to_work_context |
| **Download:** | [36_skills_to_work_context.sql](/dl_files/database/db_30_1_mysql/36_skills_to_work_context.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| skills_element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| work_context_element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |

This file contains linkages between skills and relevant work context. Occupation-specific ratings for the listed elements may be found in the [*Skills*](skills.html "Skills") and [*Work Context*](work_context.html "Work Context") files. Linkages were developed by a panel of experienced industrial/organizational psychologists, and are used in the development of analyst occupational skills ratings.

The file is displayed in two tab delimited fields with the columns named Skills Element ID and Work Context Element ID. The two fields are represented by one row. There are a total of 96 rows of data in this file.

For more information, see:
* [O*NET Analyst Occupational Skills Ratings: Procedures Update](https://www.onetcenter.org/reports/AOSkills_ProcUpdate.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 24.2 | Added as a new file |
| 24.3 - 30.1 | No structure changes |

### Data Example - skills_to_work_context:

| skills_element_id | work_context_element_id |
| --- | --- |
| 2.A.1.a | 4.C.1.a.2.h |
| 2.A.1.b | 4.C.1.a.2.c |
| 2.A.1.b | 4.C.1.a.2.f |
| 2.A.1.b | 4.C.1.a.2.l |
| 2.A.1.b | 4.C.1.a.4 |

---

# survey_booklet_locations.md

# Survey Booklet Locations

* [Excel](/dictionary/30.1/excel/survey_booklet_locations.html)
* [Text](/dictionary/30.1/text/survey_booklet_locations.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/survey_booklet_locations.html)
* [Oracle](/dictionary/30.1/oracle/survey_booklet_locations.html)

| **Purpose:** | Provide survey item numbers for O*NET Content Model elements. |
| **Table Name:** | survey_booklet_locations |
| **Download:** | [08_survey_booklet_locations.sql](/dl_files/database/db_30_1_mysql/08_survey_booklet_locations.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| survey_item_number | Character Varying(5) | Survey Booklet Location Number |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |

This file contains the Content Model elements that have corresponding survey item numbers in the Survey Booklet. Each survey item number corresponds to a survey question in the [O*NET Questionnaires](https://www.onetcenter.org/ombclearance.html). The values for incumbent data categories are percentage ratings corresponding to survey question options. Match the element ID(s) from data files to a survey item number using this file.

The file is displayed in three tab delimited fields with the columns named Element ID, Survey Item Number, and Scale ID. The three fields are represented by one row. There are a total of 211 rows of data in this file.

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 | Added as a new file |
| 5.1 - 12.0 | No structure changes |
| 13.0 | Added Scale ID column |
| 14.0 - 29.1 | No structure changes |
| 29.2 | Survey Item Number expanded from 4 characters to 5 |
| 29.3 - 30.1 | No structure changes |

### Data Example - survey_booklet_locations:

| element_id | survey_item_number | scale_id |
| --- | --- | --- |
| 2.C.1.a | KN01 | IM |
| 2.C.1.a | KN01b | LV |
| 2.C.1.b | KN02 | IM |
| 2.C.1.b | KN02b | LV |
| 2.C.1.c | KN03 | IM |
| 2.C.1.c | KN03b | LV |

---

# task_categories.md

# Task Categories

* [Excel](/dictionary/30.1/excel/task_categories.html)
* [Text](/dictionary/30.1/text/task_categories.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/task_categories.html)
* [Oracle](/dictionary/30.1/oracle/task_categories.html)

| **Purpose:** | Provide description of Task categories. |
| **Table Name:** | task_categories |
| **Download:** | [09_task_categories.sql](/dl_files/database/db_30_1_mysql/09_task_categories.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| category | Decimal(3,0) | Category value associated with Scale ID |
| category_description | Character Varying(1000) | Detail description of category associated with Scale ID |

This file contains the categories associated with the Task content area. Categories for the scale Frequency of Task (FT) are included. The file is displayed in three tab delimited fields with the columns named Scale ID, Category, and Category Description. The three fields are represented by one row. There are a total of 7 rows of data in this file.

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 13.0 | Added as a new file |
| 14.0 - 30.1 | No structure changes |

### Data Example - task_categories:

| scale_id | category | category_description |
| --- | --- | --- |
| FT | 1 | Yearly or less |
| FT | 2 | More than yearly |
| FT | 3 | More than monthly |
| FT | 4 | More than weekly |
| FT | 5 | Daily |
| FT | 6 | Several times daily |
| FT | 7 | Hourly or more |

---

# task_ratings.md

# Task Ratings

* [Excel](/dictionary/30.1/excel/task_ratings.html)
* [Text](/dictionary/30.1/text/task_ratings.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/task_ratings.html)
* [Oracle](/dictionary/30.1/oracle/task_ratings.html)

| **Purpose:** | Provide a mapping of O*NET-SOC codes (occupations) to the ratings for tasks associated with the occupation. |
| **Table Name:** | task_ratings |
| **Download:** | [18_task_ratings.sql](/dl_files/database/db_30_1_mysql/18_task_ratings.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| task_id | Decimal(8,0) | Identifies each task *(see [*Task Statements*](task_statements.html "Task Statements"))* |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| category | Decimal(3,0) | Percent frequency category *(see [*Task Categories*](task_categories.html "Task Categories"))* |
| data_value | Decimal(5,2) | Rating associated with the O*NET-SOC occupation |
| n | Decimal(4,0) | Sample size |
| standard_error | Decimal(7,4) | Standard Error |
| lower_ci_bound | Decimal(7,4) | Lower 95% confidence interval bound |
| upper_ci_bound | Decimal(7,4) | Upper 95% confidence interval bound |
| recommend_suppress | Character(1) | Low precision indicator (Y=yes, N=no) |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

This file contains the task ratings associated with each O*NET-SOC occupation. It is displayed in 12 tab delimited fields and identified using the column names provided above. Item rating level metadata is provided in columns named n, standard_error, lower_ci_bound, upper_ci_bound, recommend_suppress, date_updated, and domain_source. Refer to **[Appendix 2, *Item Rating Level Statistics - Incumbent*](appendix_incumbent.html "Appendix 2. Item Rating Level Statistics - Incumbent")** for additional information on these items. The 12 fields are represented by one row. There are a total of 161,559 rows of data in this file.

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 13.0 | Added as a new file |
| 14.0 - 28.1 | No structure changes |
| 28.2 | Standard Error, Lower CI Bound, Upper CI Bound expanded from 2 decimal places to 4 |
| 28.3 - 30.1 | No structure changes |

### Data Example - task_ratings:

| onetsoc_code | task_id | scale_id | category | data_value | n | standard_error | lower_ci_bound | upper_ci_bound | recommend_suppress | date_updated | domain_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 53-3053.00 | 23756 | FT | 1 | 0.00 | 61 | 0.0000 | NULL | NULL | N | 2025-08-01 | Incumbent |
| 53-3053.00 | 23756 | FT | 2 | 0.24 | 61 | 0.1717 | 0.0546 | 1.0082 | N | 2025-08-01 | Incumbent |
| 53-3053.00 | 23756 | FT | 3 | 4.25 | 61 | 2.8703 | 1.0727 | 15.3926 | N | 2025-08-01 | Incumbent |
| 53-3053.00 | 23756 | FT | 4 | 4.89 | 61 | 3.7881 | 0.9999 | 20.7683 | N | 2025-08-01 | Incumbent |
| 53-3053.00 | 23756 | FT | 5 | 83.26 | 61 | 11.2185 | 49.8527 | 96.1377 | N | 2025-08-01 | Incumbent |
| 53-3053.00 | 23756 | FT | 6 | 0.34 | 61 | 0.2578 | 0.0721 | 1.5488 | N | 2025-08-01 | Incumbent |
| 53-3053.00 | 23756 | FT | 7 | 7.02 | 61 | 7.1452 | 0.8384 | 40.2745 | N | 2025-08-01 | Incumbent |
| 53-3053.00 | 23756 | IM | NULL | 4.84 | 62 | 0.0722 | 4.6956 | 4.9844 | N | 2025-08-01 | Incumbent |
| 53-3053.00 | 23756 | RT | NULL | 100.00 | 66 | 0.0000 | NULL | NULL | N | 2025-08-01 | Incumbent |

---

# task_statements.md

# Task Statements

* [Excel](/dictionary/30.1/excel/task_statements.html)
* [Text](/dictionary/30.1/text/task_statements.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/task_statements.html)
* [Oracle](/dictionary/30.1/oracle/task_statements.html)

| **Purpose:** | Provide a mapping of O*NET-SOC codes (occupations) to tasks associated with the occupation. |
| **Table Name:** | task_statements |
| **Download:** | [17_task_statements.sql](/dl_files/database/db_30_1_mysql/17_task_statements.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| task_id | Decimal(8,0) | Identifies each task |
| task | Character Varying(1000) | Task statement associated with an occupation |
| task_type | Character Varying(12) | “Core” or “Supplemental” |
| incumbents_responding | Decimal(4,0) | Number of incumbents providing task information |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

This file contains the tasks associated with each O*NET-SOC occupation. The “Task Type” column identifies two categories of tasks:
* **Core** — tasks that are critical to the occupation. The criteria for these tasks are (a) relevance ≥ 67% and (b) a mean importance rating of ≥ 3.0.
* **Supplemental** — tasks that are less relevant and/or important to the occupation. Two sets of tasks are included in this category: (a) tasks rated ≥ 67% on relevance but < 3.0 on importance, and (b) tasks rated < 67% on relevance, regardless of mean importance.

The file is displayed in seven tab delimited fields with the columns named O*NET-SOC Code, Task ID, Task, Task Type, Incumbents Responding, Date, and Domain Source. The seven fields are represented by one row. There are a total of 18,796 rows of data in this file.

For more information, see:
* [Summary of Procedures for O*NET Task Updating and New Task Generation](https://www.onetcenter.org/reports/TaskUpdating.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 13.0 | Added as a new file |
| 14.0 - 30.1 | No structure changes |

### Data Example - task_statements:

| onetsoc_code | task_id | task | task_type | incumbents_responding | date_updated | domain_source |
| --- | --- | --- | --- | --- | --- | --- |
| 29-1212.00 | 22689 | Administer emergency cardiac care for life-threatening heart problems, such as cardiac arrest and heart attack. | NULL | NULL | 2025-12-01 | Analyst |
| 29-1212.00 | 22690 | Advise patients and community members concerning diet, activity, hygiene, or disease prevention. | NULL | NULL | 2025-12-01 | Analyst |
| 29-1212.00 | 22691 | Answer questions that patients have about their health and well-being. | NULL | NULL | 2025-12-01 | Analyst |
| 29-1212.00 | 22692 | Calculate valve areas from blood flow velocity measurements. | NULL | NULL | 2025-12-01 | Analyst |
| 29-1212.00 | 22693 | Compare measurements of heart wall thickness and chamber sizes to standards to identify abnormalities, using the results of an echocardiogram. | NULL | NULL | 2025-12-01 | Analyst |
| 29-1212.00 | 22694 | Conduct electrocardiogram (EKG), phonocardiogram, echocardiogram, or other cardiovascular tests to record patients' cardiac activity, using specialized electronic test equipment, recording devices, or laboratory instruments. | NULL | NULL | 2025-12-01 | Analyst |
| 29-1212.00 | 22695 | Conduct exercise electrocardiogram tests to monitor cardiovascular activity under stress. | NULL | NULL | 2025-12-01 | Analyst |

---

# tasks_to_dwas.md

# Tasks to DWAs

* [Excel](/dictionary/30.1/excel/tasks_to_dwas.html)
* [Text](/dictionary/30.1/text/tasks_to_dwas.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/tasks_to_dwas.html)
* [Oracle](/dictionary/30.1/oracle/tasks_to_dwas.html)

| **Purpose:** | Provide a mapping of task statements to Detailed Work Activities. |
| **Table Name:** | tasks_to_dwas |
| **Download:** | [25_tasks_to_dwas.sql](/dl_files/database/db_30_1_mysql/25_tasks_to_dwas.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| task_id | Decimal(8,0) | Identifies each task *(see [*Task Statements*](task_statements.html "Task Statements"))* |
| dwa_id | Character Varying(20) | Identifies each Detailed Work Activity *(see [*DWA Reference*](dwa_reference.html "DWA Reference"))* |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

This file maps each Detailed Work Activity (DWA) to the task statements, and consequently to the O*NET-SOC occupations, requiring that activity. Each DWA is mapped to multiple task statements, and each referenced task statement is mapped to one or more DWAs.

The file is displayed in five tab delimited fields with the columns named O*NET-SOC Code, Task ID, DWA ID, Date, and Domain Source. The five fields are represented by one row. There are a total of 23,850 rows of data in this file.

For more information, see:
* [O*NET Work Activities Project Technical Report](https://www.onetcenter.org/reports/DWA_2014.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 18.1 | Added as a new file |
| 19.0 - 30.1 | No structure changes |

### Data Example - tasks_to_dwas:

| onetsoc_code | task_id | dwa_id | date_updated | domain_source |
| --- | --- | --- | --- | --- |
| 25-3011.00 | 6824 | 4.A.3.b.6.I12.D04 | 2014-03-01 | Analyst |
| 25-3011.00 | 6825 | 4.A.1.a.2.I06.D03 | 2014-03-01 | Analyst |
| 25-3011.00 | 6825 | 4.A.2.a.1.I03.D04 | 2014-03-01 | Analyst |
| 25-3011.00 | 6826 | 4.A.2.b.2.I15.D06 | 2014-03-01 | Analyst |
| 25-3011.00 | 6827 | 4.A.4.b.3.I02.D06 | 2014-03-01 | Analyst |

---

# technology_skills.md

# Technology Skills

* [Excel](/dictionary/30.1/excel/technology_skills.html)
* [Text](/dictionary/30.1/text/technology_skills.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/technology_skills.html)
* [Oracle](/dictionary/30.1/oracle/technology_skills.html)

| **Purpose:** | Provide Technology Skills examples. |
| **Table Name:** | technology_skills |
| **Download:** | [31_technology_skills.sql](/dl_files/database/db_30_1_mysql/31_technology_skills.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| example | Character Varying(150) | Technology skill example |
| commodity_code | Decimal(8,0) | UNSPSC commodity code *(see [*UNSPSC Reference*](unspsc_reference.html "UNSPSC Reference"))* |
| hot_technology | Character(1) | Whether example is classified as a hot technology (Y=yes, N=no) |
| in_demand | Character(1) | Whether example is classified as in demand for the occupation (Y=yes, N=no) |

This file contains the Technology Skills examples, including hot and in-demand technologies, associated with O*NET-SOC occupations. The columns “Commodity Code” and “Commodity Title” classify the example under the United Nations Standard Products and Services Code (UNSPSC). See the [*UNSPSC Reference*](unspsc_reference.html "UNSPSC Reference") section for more information. The “Hot Technology” column indicates requirements frequently included across all employer job postings. A concise list of all hot technologies may be downloaded from [O*NET OnLine](https://www.onetonline.org/search/hot_tech/). The “In Demand” column indicates requirements frequently included in employer job postings for the particular occupation.

We welcome feedback on the Technology Skills database. We accept suggestions for new technology skills via our [feedback process](https://www.onetcenter.org/t2_feedback.html). Suggestions will be considered for a future update of the Technology Skills database.

The file is displayed in five tab delimited fields with the columns named O*NET-SOC Code, Example, Commodity Code, Hot Technology, and In Demand. The five fields are represented by one row. There are a total of 32,773 rows of data in this file.

For more information, see:
* [Hot Technologies and In Demand Technology Skills within the O*NET System](https://www.onetcenter.org/reports/Hot_Technologies_Demand.html)
* [O*NET Center Tools and Technology Quality Control Processes](https://www.onetcenter.org/reports/T2_QC.html)
* [O*NET Tools and Technology: A Synopsis of Data Development Procedures](https://www.onetcenter.org/reports/T2Development.html)
* [Identification of “Hot Technologies” within the O*NET® System](https://www.onetcenter.org/reports/Hot_Technologies.html)
* [Tools and Technology Search](https://www.onetcenter.org/reports/T2_Search.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 23.2 | Added as a new file |
| 23.3 - 27.0 | No structure changes |
| 27.1 | “In Demand” column added |
| 27.2 - 30.1 | No structure changes |

### Data Example - technology_skills:

| onetsoc_code | example | commodity_code | hot_technology | in_demand |
| --- | --- | --- | --- | --- |
| 11-2011.00 | Actuate BIRT | 43232314 | N | N |
| 11-2011.00 | Adobe Acrobat | 43232202 | Y | N |
| 11-2011.00 | Adobe Acrobat Reader | 43232202 | N | N |
| 11-2011.00 | Adobe After Effects | 43232103 | Y | N |
| 11-2011.00 | Adobe Creative Cloud software | 43232102 | Y | N |

---

# tools_used.md

# Tools Used

* [Excel](/dictionary/30.1/excel/tools_used.html)
* [Text](/dictionary/30.1/text/tools_used.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/tools_used.html)
* [Oracle](/dictionary/30.1/oracle/tools_used.html)

| **Purpose:** | Provide Tools Used examples. |
| **Table Name:** | tools_used |
| **Download:** | [32_tools_used.sql](/dl_files/database/db_30_1_mysql/32_tools_used.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| example | Character Varying(150) | Tool example |
| commodity_code | Decimal(8,0) | UNSPSC commodity code *(see [*UNSPSC Reference*](unspsc_reference.html "UNSPSC Reference"))* |

*No longer updated or displayed in O*NET websites*

This file contains the Tools Used examples associated with O*NET-SOC occupations. The columns “Commodity Code” and “Commodity Title” classify the example under the United Nations Standard Products and Services Code (UNSPSC). See the [*UNSPSC Reference*](unspsc_reference.html "UNSPSC Reference") section for more information.

The file is displayed in three tab delimited fields with the columns named O*NET-SOC Code, Example, and Commodity Code. The three fields are represented by one row. There are a total of 41,662 rows of data in this file.

For more information, see:
* [O*NET Center Tools and Technology Quality Control Processes](https://www.onetcenter.org/reports/T2_QC.html)
* [O*NET Tools and Technology: A Synopsis of Data Development Procedures](https://www.onetcenter.org/reports/T2Development.html)
* [Tools and Technology Search](https://www.onetcenter.org/reports/T2_Search.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 23.2 | Added as a new file |
| 23.3 - 30.1 | No structure changes |

### Data Example - tools_used:

| onetsoc_code | example | commodity_code |
| --- | --- | --- |
| 11-2011.00 | Computer data input scanners | 43211711 |
| 11-2011.00 | Desktop computers | 43211507 |
| 11-2011.00 | Handheld computers | 43211715 |
| 11-2011.00 | Laptop computers | 43211503 |
| 11-2011.00 | Laser facsimile machines | 44101508 |

---

# unspsc_reference.md

# UNSPSC Reference

* [Excel](/dictionary/30.1/excel/unspsc_reference.html)
* [Text](/dictionary/30.1/text/unspsc_reference.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/unspsc_reference.html)
* [Oracle](/dictionary/30.1/oracle/unspsc_reference.html)

| **Purpose:** | Provide relevant aspects of the UNSPSC taxonomy. |
| **Table Name:** | unspsc_reference |
| **Download:** | [28_unspsc_reference.sql](/dl_files/database/db_30_1_mysql/28_unspsc_reference.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| commodity_code | Decimal(8,0) | UNSPSC commodity code |
| commodity_title | Character Varying(150) | UNSPSC commodity title |
| class_code | Decimal(8,0) | UNSPSC class code |
| class_title | Character Varying(150) | UNSPSC class title |
| family_code | Decimal(8,0) | UNSPSC family code |
| family_title | Character Varying(150) | UNSPSC family title |
| segment_code | Decimal(8,0) | UNSPSC segment code |
| segment_title | Character Varying(150) | UNSPSC segment title |

This file contains a listing of commodities in the United Nations Standard Products and Services Code (UNSPSC), version 260801. The UNSPSC is a four-level taxonomy for the classification of products and services, provided by the [United Nations Development Programme](http://www.unspsc.org/). In the taxonomy, the Segment is the most general element and the Commodity is the most specific. One example is listed below:

| Segment: | 43000000 | Information Technology Broadcasting and Telecommunications |
|---|---|---|
| Family: | 43230000 | Software |
| Class: | 43232100 | Content authoring and editing software |
| Commodity: | 43232104 | Word processing software |

Each technology or tool example is classified under this taxonomy; the “Commodity Code” and “Commodity Title” columns in the [*Technology Skills*](technology_skills.html "Technology Skills") and [*Tools Used*](tools_used.html "Tools Used") files can be used as a cross-reference into this file. The file is displayed in 8 tab delimited fields with the columns named Commodity Code, Commodity Title, Class Code, Class Title, Family Code, Family Title, Segment Code, and Segment Title. The 8 fields are represented by one row. There are a total of 4,264 rows of data in this file.

For more information, see:
* [O*NET Center Tools and Technology Quality Control Processes](https://www.onetcenter.org/reports/T2_QC.html)
* [O*NET Tools and Technology: A Synopsis of Data Development Procedures](https://www.onetcenter.org/reports/T2Development.html)
* [Identification of “Hot Technologies” within the O*NET® System](https://www.onetcenter.org/reports/Hot_Technologies.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 20.1 | Added as a new file |
| 20.2 - 30.1 | No structure changes |

### Data Example - unspsc_reference:

| commodity_code | commodity_title | class_code | class_title | family_code | family_title | segment_code | segment_title |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 12131704 | Explosive initiators | 12131700 | Igniters | 12130000 | Explosive materials | 12000000 | Chemicals including Bio Chemicals and Gas Materials |
| 12131707 | Lighters | 12131700 | Igniters | 12130000 | Explosive materials | 12000000 | Chemicals including Bio Chemicals and Gas Materials |
| 14111513 | Ledger paper | 14111500 | Printing and writing paper | 14110000 | Paper products | 14000000 | Paper Materials and Products |
| 14111802 | Receipts or receipt books | 14111800 | Business use papers | 14110000 | Paper products | 14000000 | Paper Materials and Products |

---

# work_activities.md

# Work Activities

* [Excel](/dictionary/30.1/excel/work_activities.html)
* [Text](/dictionary/30.1/text/work_activities.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/work_activities.html)
* [Oracle](/dictionary/30.1/oracle/work_activities.html)

| **Purpose:** | Provide a mapping of O*NET-SOC codes (occupations) to Work Activity ratings. |
| **Table Name:** | work_activities |
| **Download:** | [19_work_activities.sql](/dl_files/database/db_30_1_mysql/19_work_activities.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| data_value | Decimal(5,2) | Rating associated with the O*NET-SOC occupation |
| n | Decimal(4,0) | Sample size |
| standard_error | Decimal(7,4) | Standard Error |
| lower_ci_bound | Decimal(7,4) | Lower 95% confidence interval bound |
| upper_ci_bound | Decimal(7,4) | Upper 95% confidence interval bound |
| recommend_suppress | Character(1) | Low precision indicator (Y=yes, N=no) |
| not_relevant | Character(1) | Not relevant for the occupation (Y=yes, N=no) |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

This file contains the Content Model Work Activity data associated with each O*NET-SOC occupation. It is displayed in 12 tab delimited fields and identified using the column names provided above. Item rating level metadata is provided in columns named n, standard_error, lower_ci_bound, upper_ci_bound, recommend_suppress, not_relevant, date_updated, and domain_source. Refer to **[Appendix 2, *Item Rating Level Statistics - Incumbent*](appendix_incumbent.html "Appendix 2. Item Rating Level Statistics - Incumbent")** for additional information on these items. The 12 fields are represented by one row. There are a total of 73,308 rows of data in this file.

For more information, see:
* [O*NET Work Activities Project Technical Report](https://www.onetcenter.org/reports/DWA_2014.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 | Date and Source columns added |
| 5.1 | Columns added for N, Standard Error, Lower CI Bound, Upper CI Bound, Recommend Suppress, and Not Relevant |
| 6.0 - 28.1 | No structure changes |
| 28.2 | Standard Error, Lower CI Bound, Upper CI Bound expanded from 2 decimal places to 4 |
| 28.3 - 30.1 | No structure changes |

### Data Example - work_activities:

| onetsoc_code | element_id | scale_id | data_value | n | standard_error | lower_ci_bound | upper_ci_bound | recommend_suppress | not_relevant | date_updated | domain_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 17-2121.00 | 4.A.1.a.1 | IM | 4.22 | 18 | NULL | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 17-2121.00 | 4.A.1.a.1 | LV | 5.17 | 18 | NULL | NULL | NULL | NULL | N | 2025-08-01 | Occupational Expert |
| 17-2121.00 | 4.A.1.a.2 | IM | 3.12 | 17 | NULL | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 17-2121.00 | 4.A.1.a.2 | LV | 3.94 | 17 | NULL | NULL | NULL | NULL | N | 2025-08-01 | Occupational Expert |
| 17-2121.00 | 4.A.1.b.1 | IM | 3.83 | 18 | NULL | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 17-2121.00 | 4.A.1.b.1 | LV | 5.00 | 18 | NULL | NULL | NULL | NULL | N | 2025-08-01 | Occupational Expert |
| 17-2121.00 | 4.A.1.b.2 | IM | 3.76 | 17 | NULL | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 17-2121.00 | 4.A.1.b.2 | LV | 4.35 | 17 | NULL | NULL | NULL | NULL | N | 2025-08-01 | Occupational Expert |
| 17-2121.00 | 4.A.1.b.3 | IM | 3.17 | 18 | NULL | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 17-2121.00 | 4.A.1.b.3 | LV | 3.89 | 18 | NULL | NULL | NULL | NULL | N | 2025-08-01 | Occupational Expert |
| 17-2121.00 | 4.A.2.a.1 | IM | 3.17 | 18 | NULL | NULL | NULL | NULL | NULL | 2025-08-01 | Occupational Expert |
| 17-2121.00 | 4.A.2.a.1 | LV | 3.94 | 18 | NULL | NULL | NULL | NULL | N | 2025-08-01 | Occupational Expert |

---

# work_context.md

# Work Context

* [Excel](/dictionary/30.1/excel/work_context.html)
* [Text](/dictionary/30.1/text/work_context.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/work_context.html)
* [Oracle](/dictionary/30.1/oracle/work_context.html)

| **Purpose:** | Provide a mapping of O*NET-SOC codes (occupations) to Work Context ratings. |
| **Table Name:** | work_context |
| **Download:** | [20_work_context.sql](/dl_files/database/db_30_1_mysql/20_work_context.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| category | Decimal(3,0) | Percent frequency category *(see [*Work Context Categories*](work_context_categories.html "Work Context Categories"))* |
| data_value | Decimal(5,2) | Rating associated with the O*NET-SOC occupation |
| n | Decimal(4,0) | Sample size |
| standard_error | Decimal(7,4) | Standard Error |
| lower_ci_bound | Decimal(7,4) | Lower 95% confidence interval bound |
| upper_ci_bound | Decimal(7,4) | Upper 95% confidence interval bound |
| recommend_suppress | Character(1) | Low precision indicator (Y=yes, N=no) |
| not_relevant | Character(1) | Not relevant for the occupation (Y=yes, N=no) |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

This file contains the Content Model Work Context data associated with each O*NET-SOC occupation. It is displayed in 13 tab delimited fields and identified using the column names provided above. Item rating level metadata is provided in columns named n, standard_error, lower_ci_bound, upper_ci_bound, recommend_suppress, not_relevant, date_updated, and domain_source. Refer to **[Appendix 2, *Item Rating Level Statistics - Incumbent*](appendix_incumbent.html "Appendix 2. Item Rating Level Statistics - Incumbent")** for additional information on these items. The 13 fields are represented by one row. There are a total of 297,676 rows of data in this file.

The column named Data Value provides both the mean rating (indicated by the value CX in the Scale ID column) and the percent of respondents endorsing each category (indicated by CXP in the Scale ID column).

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 | Date and Source columns added |
| 5.1 | Columns added for N, Standard Error, Lower CI Bound, Upper CI Bound, Recommend Suppress, and Not Relevant |
| 6.0 - 28.1 | No structure changes |
| 28.2 | Standard Error, Lower CI Bound, Upper CI Bound expanded from 2 decimal places to 4 |
| 28.3 - 30.1 | No structure changes |

### Data Example - work_context:

| onetsoc_code | element_id | scale_id | category | data_value | n | standard_error | lower_ci_bound | upper_ci_bound | recommend_suppress | not_relevant | date_updated | domain_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 47-2141.00 | 4.C.3.d.8 | CT | NULL | 1.99 | 20 | 0.2281 | 1.5163 | 2.4712 | N | NULL | 2025-08-01 | Incumbent |
| 47-2141.00 | 4.C.3.d.8 | CTP | 1 | 17.03 | 20 | 17.7643 | 1.4564 | 74.0353 | Y | NULL | 2025-08-01 | Incumbent |
| 47-2141.00 | 4.C.3.d.8 | CTP | 2 | 66.56 | 20 | 23.7009 | 17.6484 | 94.8695 | Y | NULL | 2025-08-01 | Incumbent |
| 47-2141.00 | 4.C.3.d.8 | CTP | 3 | 16.41 | 20 | 15.0155 | 1.9455 | 65.9997 | Y | NULL | 2025-08-01 | Incumbent |

---

# work_context_categories.md

# Work Context Categories

* [Excel](/dictionary/30.1/excel/work_context_categories.html)
* [Text](/dictionary/30.1/text/work_context_categories.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/work_context_categories.html)
* [Oracle](/dictionary/30.1/oracle/work_context_categories.html)

| **Purpose:** | Provide description of Work Context categories. |
| **Table Name:** | work_context_categories |
| **Download:** | [10_work_context_categories.sql](/dl_files/database/db_30_1_mysql/10_work_context_categories.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| category | Decimal(3,0) | Category value associated with element |
| category_description | Character Varying(1000) | Detail description of category associated with element |

This file contains the categories associated with the Work Context content area. Categories for the following scales are included: Context (CXP) and Context Category (CTP). The file includes categories utilized in the data collection survey where the category descriptions are variable and item specific. The file is displayed in four tab delimited fields with the columns named Element ID, Scale ID, Category, and Category Description. The four fields are represented by one row. There are a total of 281 rows of data in this file.

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 9.0 | Added as a new file |
| 10.0 - 30.1 | No structure changes |

### Data Example - work_context_categories:

| element_id | scale_id | category | category_description |
| --- | --- | --- | --- |
| 4.C.1.a.2.l | CXP | 1 | Never |
| 4.C.1.a.2.l | CXP | 2 | Once a year or more but not every month |
| 4.C.1.a.2.l | CXP | 3 | Once a month or more but not every week |
| 4.C.1.a.2.l | CXP | 4 | Once a week or more but not every day |
| 4.C.1.a.2.l | CXP | 5 | Every day |
| 4.C.1.a.4 | CXP | 1 | No contact with others |
| 4.C.1.a.4 | CXP | 2 | Occasional contact with others |
| 4.C.1.a.4 | CXP | 3 | Contact with others about half the time |
| 4.C.1.a.4 | CXP | 4 | Contact with others most of the time |
| 4.C.1.a.4 | CXP | 5 | Constant contact with others |

---

# work_styles.md

# Work Styles

* [Excel](/dictionary/30.1/excel/work_styles.html)
* [Text](/dictionary/30.1/text/work_styles.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/work_styles.html)
* [Oracle](/dictionary/30.1/oracle/work_styles.html)

| **Purpose:** | Provide a mapping of O*NET-SOC codes (occupations) to Work Styles ratings. |
| **Table Name:** | work_styles |
| **Download:** | [21_work_styles.sql](/dl_files/database/db_30_1_mysql/21_work_styles.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| data_value | Decimal(5,2) | Rating associated with the O*NET-SOC occupation |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

This file contains the Work Styles Impact ratings and Distinctiveness Rank assignments for each O*NET-SOC occupation. Work Styles ratings are presented as two scales. WI reports the Impact rating of each Work Style on performance of an occupation’s work activities and in relevant work contexts, from -3.00 (very detrimental) to +3.00 (very beneficial). DR reports the “distinctiveness rank” of a Work Style for an occupation, which presents up to 10 beneficial Work Styles which distinguish an occupation from others. A DR rating of 0.00 indicates the Work Style is not part of the ranked list.

The file is displayed in six tab delimited fields with the columns named O*NET-SOC Code, Element ID, Scale ID, Data Value, Date, and Domain Source. The six fields are represented by one row. There are a total of 37,422 rows of data in this file.

For more information, see:
* [Updating Higher-order Work Style Dimensions in the O*NET Work Styles Taxonomy](https://www.onetcenter.org/reports/Higher_Order_Styles.html)
* [Revisiting the Work Styles Domain of the O*NET Content Model](https://www.onetcenter.org/reports/Work_Styles_New.html)
* [Using a Hybrid Artificial Intelligence-Expert Method to Develop Work Style Ratings for the O*NET Database](https://www.onetcenter.org/reports/Hybrid_AI_Ratings.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 | Added as a new file |
| 5.1 | Columns added for N, Standard Error, Lower CI Bound, Upper CI Bound, and Recommend Suppress |
| 6.0 - 28.1 | No structure changes |
| 28.2 | Standard Error, Lower CI Bound, Upper CI Bound expanded from 2 decimal places to 4 |
| 28.3 - 30.0 | No structure changes |
| 30.1 | Columns removed for N, Standard Error, Lower CI Bound, Upper CI Bound, and Recommend Suppress |

### Data Example - work_styles:

| onetsoc_code | element_id | scale_id | data_value | date_updated | domain_source |
| --- | --- | --- | --- | --- | --- |
| 29-1141.01 | 1.D.1.a | DR | 0.00 | 2025-12-01 | AI/Expert |
| 29-1141.01 | 1.D.1.a | WI | 1.10 | 2025-12-01 | AI/Expert |
| 29-1141.01 | 1.D.1.b | DR | 0.00 | 2025-12-01 | AI/Expert |
| 29-1141.01 | 1.D.1.b | WI | 1.98 | 2025-12-01 | AI/Expert |
| 29-1141.01 | 1.D.1.c | DR | 0.00 | 2025-12-01 | AI/Expert |

---

# work_values.md

# Work Values

* [Excel](/dictionary/30.1/excel/work_values.html)
* [Text](/dictionary/30.1/text/work_values.html)
* [MySQL](#)
* [SQL Server](/dictionary/30.1/mssql/work_values.html)
* [Oracle](/dictionary/30.1/oracle/work_values.html)

| **Purpose:** | Provide a mapping of O*NET-SOC codes (occupations) to Work Values ratings. |
| **Table Name:** | work_values |
| **Download:** | [22_work_values.sql](/dl_files/database/db_30_1_mysql/22_work_values.sql) |

### Structure and Description:

| Column | Type | Column Content |
| --- | --- | --- |
| onetsoc_code | Character(10) | O*NET-SOC Code *(see [*Occupation Data*](occupation_data.html "Occupation Data"))* |
| element_id | Character Varying(20) | Content Model Outline Position *(see [*Content Model Reference*](content_model_reference.html "Content Model Reference"))* |
| scale_id | Character Varying(3) | Scale ID *(see [*Scales Reference*](scales_reference.html "Scales Reference"))* |
| data_value | Decimal(5,2) | Rating associated with the O*NET-SOC occupation |
| date_updated | Date | Date when data was updated |
| domain_source | Character Varying(30) | Source of the data |

*No longer updated or displayed in O*NET websites*

This file contains the Content Model Work Values data associated with each O*NET- SOC occupation. The column named Data Value provides both the mean extent rating (indicated by the value EX in the Scale ID column) and the top three high-point values for respondents endorsing each occupation (indicated by VH in the Scale ID Column).

The high-point values represent the following elements:

|   | 0.00 = No high point available |   |
|---|---|---|
|   | 1.00 = Achievement |   |
|   | 2.00 = Working Conditions |   |
|   | 3.00 = Recognition |   |
|   | 4.00 = Relationships |   |
|   | 5.00 = Support |   |
|   | 6.00 = Independence |   |

The file is displayed in six tab delimited fields with the columns named O*NET-SOC Code, Element ID, Scale ID, Data Value, Date, and Domain Source. The six fields are represented by one row. There are a total of 7,866 rows of data in this file.

For more information, see:
* [Second Generation Occupational Value Profiles for the O*NET System: Summary](https://www.onetcenter.org/reports/SecondOVP_Summary.html)
* [Occupational Value Profiles for New and Emerging Occupations in the O*NET System: Summary](https://www.onetcenter.org/reports/OVP_NewEmerging.html)

### File Structure Changes:

| Release Number | Description of Change |
| --- | --- |
| 5.0 | Date and Source columns added |
| 5.1 - 30.1 | No structure changes |

### Data Example - work_values:

| onetsoc_code | element_id | scale_id | data_value | date_updated | domain_source |
| --- | --- | --- | --- | --- | --- |
| 19-3033.00 | 1.B.2.a | EX | 5.83 | 2020-11-01 | Analyst - Transition |
| 19-3033.00 | 1.B.2.b | EX | 5.75 | 2020-11-01 | Analyst - Transition |
| 19-3033.00 | 1.B.2.c | EX | 5.33 | 2020-11-01 | Analyst - Transition |
| 19-3033.00 | 1.B.2.d | EX | 6.83 | 2020-11-01 | Analyst - Transition |
| 19-3033.00 | 1.B.2.e | EX | 3.17 | 2020-11-01 | Analyst - Transition |
| 19-3033.00 | 1.B.2.f | EX | 6.00 | 2020-11-01 | Analyst - Transition |
| 19-3033.00 | 1.B.2.g | VH | 4.00 | 2020-11-01 | Analyst - Transition |
| 19-3033.00 | 1.B.2.h | VH | 6.00 | 2020-11-01 | Analyst - Transition |
| 19-3033.00 | 1.B.2.i | VH | 1.00 | 2020-11-01 | Analyst - Transition |
