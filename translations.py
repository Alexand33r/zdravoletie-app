"""
Bilingual (English / Bulgarian) string table for the Zdravoletie dashboard.
All user-facing strings live here. No prediction logic or data processing.

Usage:
    from translations import TRANSLATIONS
    text = TRANSLATIONS["some_key"]["en"]

Or via the get_text() helper in app_utils:
    from app_utils import get_text
    label = get_text("some_key", lang)
"""

TRANSLATIONS: dict[str, dict[str, str]] = {

    # ── App-wide ──────────────────────────────────────────────────────────────

    "app_title": {
        "en": "Zdravoletie AI",
        "bg": "Zdravoletie AI",
    },
    "disclaimer": {
        "en": "This tool approximates Anovator's bodyAge score. It does not provide medical advice.",
        "bg": "Този инструмент приближава оценката bodyAge на Anovator. Не предоставя медицински съвет.",
    },

    # ── Landing page ──────────────────────────────────────────────────────────

    "home_heading": {
        "en": "Zdravoletie Biometric Intelligence",
        "bg": "Zdravoletie — Биометричен Анализ",
    },
    "home_tagline": {
        "en": (
            "Reverse-engineer and interpret the Anovator **bodyAge** score from raw biometric inputs. "
            "Select an existing client, upload a new scan, or compare a client to the population."
        ),
        "bg": (
            "Анализирайте и интерпретирайте оценката **bodyAge** на Anovator от необработени биометрични данни. "
            "Изберете съществуващ клиент, качете ново сканиране или сравнете клиент с популацията."
        ),
    },
    "age_gap_note": {
        "en": (
            "**Age gap** = bodyAge − chronological age. "
            "Positive means the Anovator system scores the client as biologically older than their actual age."
        ),
        "bg": (
            "**Разлика в телесната възраст** = bodyAge − хронологична възраст. "
            "Положителна стойност означава, че Anovator оценява клиента като биологично по-стар от действителната му възраст."
        ),
    },
    "nav_individual_title": {
        "en": "Individual Report",
        "bg": "Индивидуален Доклад",
    },
    "nav_individual_desc": {
        "en": "Select an existing client from the 158-record database, run intervention simulations, and view SHAP feature attributions.",
        "bg": "Изберете съществуващ клиент от базата данни с 158 записа, симулирайте интервенции и вижте SHAP анализ.",
    },
    "nav_individual_btn": {
        "en": "Open Individual Report",
        "bg": "Индивидуален доклад",
    },
    "nav_upload_title": {
        "en": "Upload New Scan",
        "bg": "Качи Ново Сканиране",
    },
    "nav_upload_desc": {
        "en": "Upload a CSV export from an Anovator scan session to analyse a new client not in the training database.",
        "bg": "Качете CSV файл от сесия на Anovator за анализ на нов клиент, който не е в базата данни.",
    },
    "nav_upload_btn": {
        "en": "Open Upload",
        "bg": "Качи сканиране",
    },
    "nav_population_title": {
        "en": "Population View",
        "bg": "Преглед на Популацията",
    },
    "nav_population_desc": {
        "en": "See where the currently selected or uploaded client sits in the age gap distribution of all 158 training records.",
        "bg": "Вижте позицията на текущия клиент в разпределението на разликата в телесната възраст на всички 158 записа.",
    },
    "nav_population_btn": {
        "en": "Open Population View",
        "bg": "Преглед на популацията",
    },
    "nav_export_title": {
        "en": "Export PDF",
        "bg": "Изтегли PDF",
    },
    "nav_export_desc": {
        "en": "Download a one-page PDF report with the age gap result, SHAP chart, and population histogram.",
        "bg": "Изтеглете едностраничен PDF доклад с резултата, SHAP диаграма и хистограма на популацията.",
    },
    "nav_export_btn": {
        "en": "Open PDF Export",
        "bg": "Изтегли PDF",
    },
    "home_tip": {
        "en": (
            "Start with **Individual Report** to select an existing client, "
            "or **Upload New Scan** to analyse a new one. "
            "Population View and PDF Export require an active client selection."
        ),
        "bg": (
            "Започнете с **Индивидуален доклад** за избор на съществуващ клиент "
            "или с **Качи ново сканиране** за анализ на нов. "
            "Прегледът на популацията и PDF експортът изискват активен избор на клиент."
        ),
    },
    "footer": {
        "en": "Powered by Anovator data • Fontys University of Applied Sciences 2026",
        "bg": "Базирано на данни от Anovator • Fontys University of Applied Sciences 2026",
    },

    # ── Individual Report page ─────────────────────────────────────────────────

    "page_individual_title": {
        "en": "Individual Report",
        "bg": "Индивидуален Доклад",
    },
    "page_individual_desc": {
        "en": "Select a client from the population database. Use the sliders to simulate interventions.",
        "bg": "Изберете клиент от базата данни. Използвайте плъзгачите за симулиране на интервенции.",
    },
    "sidebar_client_header": {
        "en": "Client Selection",
        "bg": "Избор на Клиент",
    },
    "lbl_client_name": {
        "en": "Client name",
        "bg": "Клиент",
    },
    "lbl_scan_date": {
        "en": "Scan date",
        "bg": "Дата на сканиране",
    },
    "sidebar_simulate_header": {
        "en": "Simulate Intervention",
        "bg": "Симулация на Интервенция",
    },
    "slider_fat_loss": {
        "en": "Target fat loss (kg)",
        "bg": "Намаление на мазнини (кг)",
    },
    "slider_muscle_gain": {
        "en": "Target muscle gain (kg)",
        "bg": "Увеличаване на мускули (кг)",
    },
    "slider_waist": {
        "en": "Waist circumference reduction (cm)",
        "bg": "Намаление на обиколка на талия (см)",
    },
    "metric_baseline_gap": {
        "en": "Baseline age gap",
        "bg": "Базова разлика",
    },
    "metric_simulated_gap": {
        "en": "Simulated age gap",
        "bg": "Симулирана разлика",
    },
    "metric_potential_gain": {
        "en": "Potential gain",
        "bg": "Потенциална печалба",
    },
    "section_feature_contributions": {
        "en": "Feature Contributions (Simulated Scan)",
        "bg": "Принос на Характеристиките (Симулирано Сканиране)",
    },
    "shap_caption_individual": {
        "en": (
            "SHAP values quantify each feature's contribution to the predicted age gap. "
            "Red features increase the predicted gap; blue features reduce it. Values are in years."
        ),
        "bg": (
            "Стойностите на SHAP показват приноса на всяка характеристика към предсказаната разлика. "
            "Червените увеличават разликата; сините я намаляват. Стойностите са в години."
        ),
    },
    "expander_raw_scan": {
        "en": "Raw scan values",
        "bg": "Необработени стойности от сканирането",
    },
    "spinner_computing": {
        "en": "Computing prediction...",
        "bg": "Изчисляване...",
    },
    "spinner_simulation": {
        "en": "Running simulation...",
        "bg": "Симулация...",
    },
    "err_prediction_failed": {
        "en": "Prediction failed: ",
        "bg": "Грешка при предсказание: ",
    },
    "err_sim_failed": {
        "en": "Simulation prediction failed: ",
        "bg": "Грешка при симулация: ",
    },

    # ── Upload New Scan page ───────────────────────────────────────────────────

    "page_upload_title": {
        "en": "Upload New Scan",
        "bg": "Качи Ново Сканиране",
    },
    "page_upload_desc": {
        "en": (
            "Upload a CSV export from an Anovator scan session. "
            "The file must contain the raw biometric columns — derived features and age gap are computed automatically."
        ),
        "bg": (
            "Качете CSV файл от сесия на Anovator. "
            "Файлът трябва да съдържа необработените биометрични колони — производните характеристики и разликата се изчисляват автоматично."
        ),
    },
    "step1_header": {
        "en": "Step 1 — Download the column template",
        "bg": "Стъпка 1 — Изтеглете шаблона с колони",
    },
    "step2_header": {
        "en": "Step 2 — Upload your completed CSV",
        "bg": "Стъпка 2 — Качете попълнения CSV файл",
    },
    "step3_header": {
        "en": "Step 3 — Select which scan to analyse",
        "bg": "Стъпка 3 — Изберете сканиране за анализ",
    },
    "step4_header": {
        "en": "Step 4 — Results",
        "bg": "Стъпка 4 — Резултати",
    },
    "btn_download_template": {
        "en": "Download CSV template",
        "bg": "Изтегли шаблон CSV",
    },
    "template_caption": {
        "en": (
            "The template contains all expected column headers. "
            "Fill in one row per scan. Columns left blank are imputed with training-set medians."
        ),
        "bg": (
            "Шаблонът съдържа всички очаквани заглавия на колони. "
            "Попълнете по един ред за всяко сканиране. Празните колони се запълват с медианите от обучението."
        ),
    },
    "upload_label": {
        "en": "Choose a CSV file",
        "bg": "Изберете CSV файл",
    },
    "upload_help": {
        "en": "Must be a UTF-8 CSV with Anovator biometric columns.",
        "bg": "Трябва да е UTF-8 CSV с биометрични колони на Anovator.",
    },
    "no_file_info": {
        "en": "No file uploaded yet.",
        "bg": "Все още няма качен файл.",
    },
    "err_parse_csv": {
        "en": "Could not parse the file as CSV: ",
        "bg": "Файлът не може да бъде прочетен като CSV: ",
    },
    "err_empty_file": {
        "en": "The uploaded file contains no data rows.",
        "bg": "Каченият файл не съдържа редове с данни.",
    },
    "err_missing_cols_title": {
        "en": "Missing required columns",
        "bg": "Липсващи задължителни колони",
    },
    "err_missing_cols_body": {
        "en": (
            "The file is missing {n} required column(s) that cannot be imputed. "
            "Download the template above, add these columns, and re-upload."
        ),
        "bg": (
            "В файла липсват {n} задължителни колони, които не могат да бъдат импутирани. "
            "Изтеглете шаблона по-горе, добавете тези колони и качете отново."
        ),
    },
    "err_missing_cols_listed": {
        "en": "Missing columns:",
        "bg": "Липсващи колони:",
    },
    "imputed_expander": {
        "en": "{n} column(s) not found — will be imputed with training medians",
        "bg": "{n} колони не са намерени — ще бъдат попълнени с медиани от обучението",
    },
    "file_loaded": {
        "en": "File loaded: {rows} row(s), {cols} columns.",
        "bg": "Файлът е зареден: {rows} ред(а), {cols} колони.",
    },
    "lbl_scan_row": {
        "en": "Scan row",
        "bg": "Ред на сканиране",
    },
    "metric_predicted_gap": {
        "en": "Predicted age gap",
        "bg": "Предсказана разлика",
    },
    "metric_interpretation": {
        "en": "Interpretation",
        "bg": "Интерпретация",
    },
    "direction_above": {
        "en": "above",
        "bg": "над",
    },
    "direction_below": {
        "en": "below",
        "bg": "под",
    },
    "interpretation_fmt": {
        "en": "{val:.2f} y {direction} chronological age",
        "bg": "{val:.2f} г. {direction} хронологичната възраст",
    },
    "spinner_prediction": {
        "en": "Running prediction...",
        "bg": "Изчисляване на предсказание...",
    },
    "section_feature_contributions_upload": {
        "en": "Feature Contributions",
        "bg": "Принос на Характеристиките",
    },
    "shap_caption_upload": {
        "en": (
            "Red features push the predicted age gap upward (biological ageing accelerators). "
            "Blue features push it downward (protective factors). Values are in years."
        ),
        "bg": (
            "Червените характеристики увеличават предсказаната разлика (ускоряват стареенето). "
            "Сините я намаляват (защитни фактори). Стойностите са в години."
        ),
    },
    "section_top_risk": {
        "en": "Top ageing accelerators",
        "bg": "Водещи ускорители на стареенето",
    },
    "section_top_protective": {
        "en": "Top protective factors",
        "bg": "Водещи защитни фактори",
    },
    "no_risk_features": {
        "en": "No features increasing the age gap.",
        "bg": "Няма характеристики, увеличаващи разликата.",
    },
    "no_protective_features": {
        "en": "No features reducing the age gap.",
        "bg": "Няма характеристики, намаляващи разликата.",
    },
    "nav_tip_upload": {
        "en": (
            "Results stored. Navigate to **Population View** to see where this client sits "
            "in the full distribution, or **Export PDF** to download a report."
        ),
        "bg": (
            "Резултатите са запазени. Отидете на **Преглед на популацията** за позицията на клиента "
            "в разпределението, или **Изтегли PDF** за доклад."
        ),
    },

    # ── Population View page ───────────────────────────────────────────────────

    "page_population_title": {
        "en": "Population View",
        "bg": "Преглед на Популацията",
    },
    "warn_no_scan": {
        "en": (
            "No active scan selected. "
            "Go to **Individual Report** to select a client from the database, "
            "or **Upload New Scan** to analyse a new scan."
        ),
        "bg": (
            "Няма активно избрано сканиране. "
            "Отидете на **Индивидуален доклад** за избор на клиент от базата данни "
            "или на **Качи ново сканиране** за анализ на ново сканиране."
        ),
    },
    "link_go_individual": {
        "en": "Go to Individual Report",
        "bg": "Към Индивидуален Доклад",
    },
    "link_go_upload": {
        "en": "Go to Upload New Scan",
        "bg": "Към Качи Ново Сканиране",
    },
    "metric_client": {
        "en": "Client",
        "bg": "Клиент",
    },
    "metric_pop_pct": {
        "en": "Population percentile",
        "bg": "Персентил на популацията",
    },
    "metric_pop_median": {
        "en": "Population median",
        "bg": "Медиана на популацията",
    },
    "metric_pop_median_help": {
        "en": "Median age gap across all 158 Anovator records.",
        "bg": "Медианна разлика в телесната възраст на всички 158 записа на Anovator.",
    },
    "hist_caption": {
        "en": (
            "The histogram shows the real age gap distribution of the 158 Anovator scan records "
            "used for model training. The dashed red line marks the current client's predicted age gap. "
            "The population percentile indicates what fraction of the 158 records have a lower age gap."
        ),
        "bg": (
            "Хистограмата показва реалното разпределение на разликата в телесната възраст на 158-те записа на Anovator, "
            "използвани за обучение на модела. Червената пунктирана линия отбелязва предсказаната разлика на текущия клиент. "
            "Персентилът показва каква част от 158-те записа имат по-ниска разлика."
        ),
    },
    "section_scatter": {
        "en": "Chronological Age vs Age Gap",
        "bg": "Хронологична Възраст и Разлика в Телесната Възраст",
    },
    "scatter_caption_with_client": {
        "en": (
            "Each point represents one of the 158 Anovator scan records. "
            "The horizontal dashed line at zero marks no difference between bodyAge and chronological age. "
            "Points above the line have a bodyAge higher than their chronological age; points below are the reverse. "
            "The red point marks the current client."
        ),
        "bg": (
            "Всяка точка представлява един от 158-те записа на Anovator. "
            "Хоризонталната пунктирана линия на нула означава, че bodyAge съвпада с хронологичната възраст. "
            "Точките над линията имат bodyAge, по-висока от хронологичната им възраст; точките под — обратното. "
            "Червената точка отбелязва текущия клиент."
        ),
    },
    "scatter_caption_no_client": {
        "en": (
            "Each point represents one of the 158 Anovator scan records. "
            "The horizontal dashed line at zero marks no difference between bodyAge and chronological age. "
            "Points above the line have a bodyAge higher than their chronological age; points below are the reverse. "
            "Client age is not available for uploaded scans; the population points are shown without a client marker."
        ),
        "bg": (
            "Всяка точка представлява един от 158-те записа на Anovator. "
            "Хоризонталната пунктирана линия на нула означава, че bodyAge съвпада с хронологичната възраст. "
            "Точките над линията имат bodyAge, по-висока от хронологичната им възраст; точките под — обратното. "
            "Възрастта на клиента не е налична за качени сканирания; показват се само точките на популацията."
        ),
    },
    "expander_pop_stats": {
        "en": "Population summary statistics",
        "bg": "Обобщена статистика на популацията",
    },
    "stat_count": {"en": "Count", "bg": "Брой"},
    "stat_mean": {"en": "Mean", "bg": "Средна стойност"},
    "stat_std": {"en": "Std dev", "bg": "Стандартно отклонение"},
    "stat_min": {"en": "Min", "bg": "Минимум"},
    "stat_p25": {"en": "P25", "bg": "25-и персентил"},
    "stat_median": {"en": "Median", "bg": "Медиана"},
    "stat_p75": {"en": "P75", "bg": "75-и персентил"},
    "stat_max": {"en": "Max", "bg": "Максимум"},
    "stat_client_gap": {"en": "Client gap", "bg": "Разлика на клиента"},
    "stat_client_pct": {"en": "Client percentile", "bg": "Персентил на клиента"},
    "stat_value": {"en": "Value", "bg": "Стойност"},

    # ── Export PDF page ────────────────────────────────────────────────────────

    "page_export_title": {
        "en": "Export PDF Report",
        "bg": "Изтегляне на PDF Доклад",
    },
    "section_report_preview": {
        "en": "Report preview",
        "bg": "Преглед на доклада",
    },
    "metric_age_gap": {
        "en": "Age gap",
        "bg": "Разлика",
    },
    "metric_source": {
        "en": "Source",
        "bg": "Източник",
    },
    "source_database": {
        "en": "Database",
        "bg": "База данни",
    },
    "source_uploaded": {
        "en": "Uploaded scan",
        "bg": "Качено сканиране",
    },
    "report_will_include": {
        "en": "The report will include:",
        "bg": "Докладът ще включва:",
    },
    "report_item_summary": {
        "en": "**Client summary**: age gap and population percentile",
        "bg": "**Обобщение на клиента**: разлика в телесната възраст и персентил",
    },
    "report_item_shap": {
        "en": "**SHAP feature contribution chart**: top 12 features by absolute contribution",
        "bg": "**SHAP диаграма на характеристиките**: топ 12 по абсолютен принос",
    },
    "report_item_hist": {
        "en": "**Population histogram**: client position in the 158-record age gap distribution",
        "bg": "**Хистограма на популацията**: позиция на клиента в разпределението на 158-те записа",
    },
    "spinner_pdf": {
        "en": "Generating PDF...",
        "bg": "Генериране на PDF...",
    },
    "err_pdf_failed": {
        "en": "PDF generation failed: ",
        "bg": "Грешката при генериране на PDF: ",
    },
    "btn_download_pdf": {
        "en": "Download PDF report",
        "bg": "Изтегли PDF доклад",
    },
    "pdf_caption": {
        "en": (
            "The PDF is generated client-side and is not stored on any server. "
            "It can be attached to client records or printed for clinical review."
        ),
        "bg": (
            "PDF файлът се генерира локално и не се съхранява на сървър. "
            "Може да се прикачи към досието на клиента или да се разпечата за клиничен преглед."
        ),
    },

    # ── About page ─────────────────────────────────────────────────────────────

    "page_about_title": {
        "en": "About This Dashboard",
        "bg": "За Таблото",
    },
    "about_intro": {
        "en": (
            "This dashboard is a research tool developed as part of a graduation thesis at "
            "Fontys University of Applied Sciences (BSc Applied Mathematics, Data Science). "
            "It provides a surrogate model and interpretability layer for the Anovator body "
            "scanning platform used at Zdravoletie, a health and rehabilitation centre in "
            "Varna, Bulgaria. The dashboard allows clinic staff to select an existing client "
            "scan, upload a new scan CSV, and view which biometric features drive the model's "
            "prediction — alongside a histogram showing where the client sits in the "
            "population of 158 recorded scans. A one-page PDF report can be downloaded for "
            "clinical records."
        ),
        "bg": (
            "Това табло е изследователски инструмент, разработен в рамките на дипломна теза към "
            "Fontys University of Applied Sciences (бакалавър по приложна математика, специализация Наука за данни). "
            "То предоставя заместващ модел и инструменти за интерпретируемост за платформата Anovator, "
            "използвана в Здраволение — център за здраве и рехабилитация във Варна, България. "
            "Таблото позволява на клиничния персонал да избере съществуващо сканиране, да качи ново "
            "в CSV формат и да прегледа кои биометрични характеристики определят предсказанието на модела — "
            "заедно с хистограма, показваща позицията на клиента сред 158 записани сканирания. "
            "Едностраничен PDF доклад може да бъде изтеглен за клиничната документация."
        ),
    },
    "about_what_predicts_title": {
        "en": "What the model predicts",
        "bg": "Какво предсказва моделът",
    },
    "about_what_predicts_body": {
        "en": (
            "The model predicts the Anovator *age gap*: the difference between the Anovator "
            "platform's proprietary bodyAge score and the client's chronological age. It does "
            "not predict clinical biological age in the medical sense — bodyAge is a "
            "commercial composite score whose formula is undisclosed and which has not been "
            "validated against mortality or morbidity endpoints. A predicted age gap of +3 "
            "years means the surrogate model estimates that the Anovator formula would return "
            "a bodyAge three years above the client's chronological age, given the biometric "
            "inputs provided. It does not mean the client is clinically three years older than "
            "their chronological age. SHAP values shown in the dashboard reflect the model's "
            "learned approximation of the Anovator formula, not independently established "
            "physiological relationships."
        ),
        "bg": (
            "Моделът предсказва *разликата в телесната възраст* (age gap) на Anovator: "
            "разликата между собствения показател bodyAge на платформата и хронологичната възраст на клиента. "
            "Той не предсказва клинична биологична възраст в медицинския смисъл — bodyAge е търговски съставен "
            "показател, чиято формула не е разкрита и не е валидирана спрямо смъртност или заболеваемост. "
            "Предсказана разлика от +3 години означава, че заместващият модел оценява, че формулата на Anovator "
            "би върнала bodyAge три години над хронологичната възраст на клиента. Това не означава, че клиентът "
            "е клинично три години по-стар. Стойностите на SHAP в таблото отразяват научената апроксимация на "
            "модела, а не независимо установени физиологични връзки."
        ),
    },
    "about_limitations_title": {
        "en": "Known limitations",
        "bg": "Известни ограничения",
    },
    "about_limitations_body": {
        "en": (
            "The surrogate model was trained on 158 scan records from 53 unique individuals "
            "at a single clinic. Mean absolute error on held-out data is approximately 2.4 "
            "years across 30 cross-validation folds, meaning individual predictions carry "
            "substantial uncertainty. Two features in the model — sportSafeRisk and "
            "sportLevel — use the value -1 as a sentinel for 'not computed' and are treated "
            "as numeric inputs; this is a known encoding artefact. Five features "
            "(leftVision, rightVision, bloodMaxPressure, bloodMinPressure, restingHeartRate) "
            "are missing in more than 88% of records and contribute negligible signal after "
            "imputation. The model should not be used as a diagnostic instrument or as a "
            "substitute for clinical assessment. It is a research prototype intended to "
            "support interpretation of Anovator outputs, not to replace them."
        ),
        "bg": (
            "Заместващият модел е обучен върху 158 сканирания на 53 уникални лица от един клиент. "
            "Средната абсолютна грешка върху данни извън обучението е приблизително 2,4 години при 30 итерации "
            "на кръстосана валидация — отделните предсказания носят значителна несигурност. "
            "Две характеристики — sportSafeRisk и sportLevel — използват стойността -1 като маркер за "
            "'непресметнато' и се третират като числови входни данни; това е известен артефакт на кодирането. "
            "Пет характеристики (leftVision, rightVision, bloodMaxPressure, bloodMinPressure, restingHeartRate) "
            "липсват при повече от 88% от записите и допринасят незначителен сигнал след импутация. "
            "Моделът не трябва да се използва като диагностичен инструмент или заместител на клинична оценка. "
            "Той е изследователски прототип за подпомагане на интерпретацията на данните от Anovator."
        ),
    },
    "about_caption": {
        "en": (
            "Source code and experiment results: graduation thesis repository, "
            "Fontys University of Applied Sciences, 2026. "
            "Model trained on data from Zdravoletie, Varna, Bulgaria."
        ),
        "bg": (
            "Изходен код и резултати: хранилище на дипломна теза, "
            "Fontys University of Applied Sciences, 2026. "
            "Моделът е обучен върху данни от Здраволение, Варна, България."
        ),
    },
}
