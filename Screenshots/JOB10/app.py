from flask import Flask, render_template, request
import mysql.connector
import pandas as pd


app = Flask(__name__)


db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "CarbonFootprint"
}


def get_dataframe(query, params=None):
    conn = mysql.connector.connect(**db_config)
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


@app.route("/")
def index():
    # pays sélectionné (via ?country=France par ex.)
    selected_country = request.args.get("country")  # None si rien choisi

    # langue UI (via ?lang=fr|en|ar)
    lang = (request.args.get("lang") or "fr").lower().strip()
    if lang not in {"fr", "en", "ar"}:
        lang = "fr"

    # puissance continue consommée (kW), par défaut 1
    power_kw_str = request.args.get("power_kw", "1")
    try:
        power_kw = float(power_kw_str)
    except ValueError:
        power_kw = 1.0

    # Traductions UI (simple i18n front)
    t = {
        "fr": {
            "title": "CarbonFootprint – Électricité",
            "header": "Calculateur d'Empreinte Carbone – Production d'électricité",
            "subtitle": "Mini-projet : analyser l'impact du mix électrique (charbon, gaz, pétrole, hydro, renouvelables, nucléaire) sur les émissions de CO₂ par kWh.",
            "filter_country": "Filtrer par pays",
            "filter_label_country": "Pays :",
            "filter_all_countries": "Tous les pays",
            "filter_label_power": "Puissance consommée (kW) :",
            "filter_current": "Filtre actuel :",
            "filter_none": "Aucun filtre : statistiques globales sur tous les pays.",
            "context_title": "Contexte du projet",
            "context_p1": "Chaque pays produit son électricité à partir d'un mélange de sources plus ou moins émettrices de CO₂. Ce projet calcule une intensité carbone estimée (en gCO₂/kWh) à partir de facteurs d'émission moyens pour chaque source d'énergie, afin de comparer rapidement les pays.",
            "context_p2": "L'intensité carbone moyenne du jeu de données est d'environ",
            "top_dirty": "Top 5 pays les plus émetteurs",
            "top_clean": "Top 5 pays les moins émetteurs",
            "country": "Pays",
            "intensity": "Intensité (gCO₂/kWh)",
            "dataset_title": "Aperçu du jeu de données CarbonFootprint",
            "dataset_sub": "Pourcentage d'utilisation de chaque source d'énergie dans la production d'électricité de quelques pays.",
            "coal": "Charbon (%)",
            "gas": "Gaz (%)",
            "oil": "Pétrole (%)",
            "hydro": "Hydro (%)",
            "renewable": "Renouvelable (%)",
            "nuclear": "Nucléaire (%)",
            "contrib_title": "Contribution des sources pour",
            "contrib_sub": "Pour chaque source : % d’utilisation × médiane d’émission = contribution spécifique en gCO₂/kWh.",
            "source": "Source de production",
            "share": "% d’utilisation",
            "median": "Médiane de gCO₂/kWh",
            "contrib": "Contribution en émission gCO₂/kWh",
            "total_emission": "Émission totale du mix électrique de",
            "annual_emission": "Pour une consommation continue de",
            "annual_emission_2": "les émissions annuelles sont :",
            "trees": "En supposant qu’un arbre absorbe 25 kg de CO₂ par an, il faudrait environ",
            "trees_2": "arbres",
            "trees_3": "pour compenser ces émissions.",
            "footer": "Projet CarbonFootprint – La Plateforme_",
            "language": "Langue",
        },
        "en": {
            "title": "CarbonFootprint – Electricity",
            "header": "Carbon Footprint Calculator – Electricity production",
            "subtitle": "Mini project: analyze how the power mix (coal, gas, oil, hydro, renewables, nuclear) impacts CO₂ emissions per kWh.",
            "filter_country": "Filter by country",
            "filter_label_country": "Country:",
            "filter_all_countries": "All countries",
            "filter_label_power": "Consumed power (kW):",
            "filter_current": "Current filter:",
            "filter_none": "No filter: global statistics across all countries.",
            "context_title": "Project context",
            "context_p1": "Each country produces electricity from a mix of sources with very different CO₂ emissions. This project estimates carbon intensity (gCO₂/kWh) using average emission factors per energy source to quickly compare countries.",
            "context_p2": "The dataset average carbon intensity is about",
            "top_dirty": "Top 5 highest emitters",
            "top_clean": "Top 5 lowest emitters",
            "country": "Country",
            "intensity": "Intensity (gCO₂/kWh)",
            "dataset_title": "CarbonFootprint dataset preview",
            "dataset_sub": "Share (%) of each energy source used in electricity production for a few countries.",
            "coal": "Coal (%)",
            "gas": "Gas (%)",
            "oil": "Oil (%)",
            "hydro": "Hydro (%)",
            "renewable": "Renewables (%)",
            "nuclear": "Nuclear (%)",
            "contrib_title": "Source contributions for",
            "contrib_sub": "For each source: share × median emissions = source contribution in gCO₂/kWh.",
            "source": "Generation source",
            "share": "Share (%)",
            "median": "Median gCO₂/kWh",
            "contrib": "Contribution (gCO₂/kWh)",
            "total_emission": "Total power-mix intensity for",
            "annual_emission": "For continuous consumption of",
            "annual_emission_2": "annual emissions are:",
            "trees": "Assuming one tree absorbs 25 kg CO₂ per year, you would need about",
            "trees_2": "trees",
            "trees_3": "to offset these emissions.",
            "footer": "CarbonFootprint Project – La Plateforme_",
            "language": "Language",
        },
        "ar": {
            "title": "البصمة الكربونية – الكهرباء",
            "header": "حاسبة البصمة الكربونية – إنتاج الكهرباء",
            "subtitle": "مشروع مصغّر: تحليل تأثير مزيج الكهرباء (الفحم، الغاز، النفط، الكهرومائي، المتجددة، النووي) على انبعاثات CO₂ لكل kWh.",
            "filter_country": "تصفية حسب الدولة",
            "filter_label_country": "الدولة:",
            "filter_all_countries": "كل الدول",
            "filter_label_power": "القدرة المستهلكة (kW):",
            "filter_current": "التصفية الحالية:",
            "filter_none": "بدون تصفية: إحصاءات عامة لكل الدول.",
            "context_title": "سياق المشروع",
            "context_p1": "تنتج كل دولة الكهرباء من مزيج من المصادر ذات انبعاثات CO₂ مختلفة. يحسب هذا المشروع كثافة كربونية تقديرية (gCO₂/kWh) اعتماداً على معاملات انبعاث متوسطة لكل مصدر لمقارنة الدول بسرعة.",
            "context_p2": "متوسط كثافة الكربون في البيانات حوالي",
            "top_dirty": "أعلى 5 دول في الانبعاثات",
            "top_clean": "أقل 5 دول في الانبعاثات",
            "country": "الدولة",
            "intensity": "الكثافة (gCO₂/kWh)",
            "dataset_title": "معاينة بيانات CarbonFootprint",
            "dataset_sub": "نسبة استخدام كل مصدر طاقة في إنتاج الكهرباء لبعض الدول.",
            "coal": "فحم (%)",
            "gas": "غاز (%)",
            "oil": "نفط (%)",
            "hydro": "كهرومائي (%)",
            "renewable": "متجددة (%)",
            "nuclear": "نووي (%)",
            "contrib_title": "مساهمة المصادر لـ",
            "contrib_sub": "لكل مصدر: نسبة الاستخدام × وسيط الانبعاث = مساهمة المصدر بوحدة gCO₂/kWh.",
            "source": "مصدر الإنتاج",
            "share": "نسبة الاستخدام (%)",
            "median": "وسيط gCO₂/kWh",
            "contrib": "المساهمة (gCO₂/kWh)",
            "total_emission": "الكثافة الإجمالية لمزيج الكهرباء لـ",
            "annual_emission": "لاستهلاك مستمر قدره",
            "annual_emission_2": "تكون الانبعاثات السنوية:",
            "trees": "بافتراض أن الشجرة تمتص 25 كغ CO₂ سنوياً، ستحتاج تقريباً إلى",
            "trees_2": "شجرة",
            "trees_3": "لمعادلة هذه الانبعاثات.",
            "footer": "مشروع CarbonFootprint – La Plateforme_",
            "language": "اللغة",
        },
    }

    # liste des pays pour la select box
    df_countries = get_dataframe("""
        SELECT DISTINCT country
        FROM Country
        ORDER BY country;
    """)
    countries = df_countries["country"].tolist()

    # filtre SQL optionnel
    where_clause = ""
    params = None
    if selected_country:
        where_clause = "WHERE country = %s"
        params = (selected_country,)

    # aperçu des données (filtré si pays choisi)
    df_preview = get_dataframe(f"""
        SELECT country, coal, gas, oil, hydro, renewable, nuclear
        FROM Country
        {where_clause}
        LIMIT 10;
    """, params=params)

    # intensité moyenne (filtrée ou globale)
    df_intensity = get_dataframe(f"""
        SELECT
          AVG(
            COALESCE(coal, 0)      * 820 +
            COALESCE(gas, 0)       * 490 +
            COALESCE(oil, 0)       * 740 +
            COALESCE(hydro, 0)     * 24  +
            COALESCE(renewable, 0) * 41  +
            COALESCE(nuclear, 0)   * 12
          ) AS avg_intensity_gco2_kwh
        FROM Country
        {where_clause};
    """, params=params)
    avg_intensity = float(df_intensity["avg_intensity_gco2_kwh"][0])

    # top 5 « sales »
    df_top_dirty = get_dataframe(f"""
        SELECT country,
          (COALESCE(coal,0)*820 + COALESCE(gas,0)*490 +
           COALESCE(oil,0)*740 + COALESCE(hydro,0)*24 +
           COALESCE(renewable,0)*41 + COALESCE(nuclear,0)*12)
          AS total_gco2_kwh
        FROM Country
        {where_clause}
        ORDER BY total_gco2_kwh DESC
        LIMIT 5;
    """, params=params)

    # top 5 « propres »
    df_top_clean = get_dataframe(f"""
        SELECT country,
          (COALESCE(coal,0)*820 + COALESCE(gas,0)*490 +
           COALESCE(oil,0)*740 + COALESCE(hydro,0)*24 +
           COALESCE(renewable,0)*41 + COALESCE(nuclear,0)*12)
          AS total_gco2_kwh
        FROM Country
        {where_clause}
        ORDER BY total_gco2_kwh ASC
        LIMIT 5;
    """, params=params)

    # ----- tableau de contribution pour le pays sélectionné -----
    contrib_table = None
    total_emission = None  # somme des contributions (gCO2/kWh)

    if selected_country:
        df_country = get_dataframe("""
            SELECT country, coal, gas, oil, hydro, renewable, nuclear
            FROM Country
            WHERE country = %s
            LIMIT 1;
        """, params=(selected_country,))

        if not df_country.empty:
            row = df_country.iloc[0]

            factors = {
                "Charbon":                {"share": row["coal"],      "median": 820},
                "Gaz naturel":            {"share": row["gas"],       "median": 490},
                "Pétrole":                {"share": row["oil"],       "median": 740},
                "Hydro":                  {"share": row["hydro"],     "median": 24},
                "Renouvelable (Solaire)": {"share": row["renewable"], "median": 41},
                "Nucléaire":              {"share": row["nuclear"],   "median": 12},
            }

            contrib_table = []
            total_emission = 0.0

            for source, vals in factors.items():
                share_pct = vals["share"] or 0      # % d'utilisation
                median = vals["median"]
                contrib = share_pct * median / 100.0  # gCO2/kWh
                total_emission += contrib

                contrib_table.append({
                    "source": source,
                    "share": share_pct,
                    "median": median,
                    "contrib": round(contrib, 2),
                })

    # ----- émission annuelle totale (kgCO2/an) + arbres -----
    annual_emission = None
    trees_needed = None

    if total_emission is not None:
        total_kg_per_kwh = total_emission / 1000.0  # g -> kg
        hours_year = 24 * 365
        annual_emission = total_kg_per_kwh * hours_year * power_kw  # kg CO2/an
        trees_needed = annual_emission / 25.0  # 25 kg CO2/an par arbre

    return render_template(
        "index.html",
        lang=lang,
        t=t[lang],
        preview=df_preview.to_dict(orient="records"),
        avg_intensity=round(avg_intensity, 2),
        top_dirty=df_top_dirty.to_dict(orient="records"),
        top_clean=df_top_clean.to_dict(orient="records"),
        countries=countries,
        selected_country=selected_country,
        contrib_table=contrib_table,
        total_emission=round(total_emission, 2) if total_emission is not None else None,
        power_kw=power_kw,
        annual_emission=round(annual_emission, 2) if annual_emission is not None else None,
        trees_needed=round(trees_needed) if trees_needed is not None else None,
    )


@app.route("/glossary")
def glossary():
    """Page statique avec les définitions des termes techniques."""
    # Langue de l'UI pour le glossaire aussi
    lang = (request.args.get("lang") or "fr").lower().strip()
    if lang not in {"fr", "en", "ar"}:
        lang = "fr"

    # Labels très simples pour le titre selon la langue
    titles = {
        "fr": "Glossaire – Énergie & empreinte carbone",
        "en": "Glossary – Energy & carbon footprint",
        "ar": "قاموس المصطلحات – الطاقة والبصمة الكربونية",
    }

    return render_template(
        "glossary.html",
        lang=lang,
        page_title=titles[lang],
    )


if __name__ == "__main__":
    app.run(debug=True)
