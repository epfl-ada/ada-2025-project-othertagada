#NLP library
import spacy
import os, codecs

import plotly.graph_objects as go


def create_collection(corpus_root):
    collection = []

    files = sorted(
        [f for f in os.listdir(corpus_root) if f.endswith(".txt")],
        key=lambda x: x.rsplit("_", 1)[-1].replace(".txt", "")
    )

    for fname in files:
        year_month = fname.rsplit("_", 1)[-1].replace(".txt","")
        with codecs.open(os.path.join(corpus_root, fname), encoding="utf8") as f:
            text = " ".join(f.read().split())
        collection.append((year_month, text))

    return collection

def plot_monthly_topic(collection, lexicon):

    nlp = spacy.load('en_core_web_lg')

    dates = []
    misogyny = []
    gamergate = []
    legal = []
    mascu = []

    for (year_month, doc) in collection:

        dates.append(year_month)

        empath_features = lexicon.analyze(
            doc[:nlp.max_length],
            categories=['misogyny', 'gamergate', 'legal', 'incel'],
            normalize=True
        )

        misogyny.append(empath_features["misogyny"])
        gamergate.append(empath_features["gamergate"])
        legal.append(empath_features["legal"])
        mascu.append(empath_features["incel"])

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dates, y=misogyny,
                             mode='lines+markers',
                             name="misogyny"))
    fig.add_trace(go.Scatter(x=dates, y=gamergate,
                             mode='lines+markers',
                             name="gamergate"))
    fig.add_trace(go.Scatter(x=dates, y=legal,
                             mode='lines+markers',
                             name="legal"))
    fig.add_trace(go.Scatter(x=dates, y=mascu,
                             mode='lines+markers',
                             name="incel"))

    fig.update_layout(
        title="r/gaming monthly topics",
        xaxis_title="Date",
        yaxis_title="Normalized Empath category frequency",
        hovermode="x unified",
        template="plotly_white"
    )

    fig.update_xaxes(tickangle=45)

    fig.write_html('docs/assets/gaming_topics_monthly.html')

    fig.show()