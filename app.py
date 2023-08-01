from flask import Flask, request, make_response, render_template, redirect, url_for
from flask.helpers import url_for
import pandas as pd
import pickle
# import warnings
# warnings.filterwarnings('ignore')

# Initialize Flask app

app = Flask(__name__)

def recomendation_obat(brand):
    drug = pickle.load(open('drug.pkl','rb'))
    similarity_matrix = pickle.load(open('similarity_matrix.pkl','rb'))
    threshold=0.35
    indexprod = drug[drug['brand'] == brand].index[0]
    similar_review = list(enumerate(similarity_matrix[indexprod]))
    filtered_sim_scores = [score for score in similar_review if score[1] > threshold]
    sorted_similar_review = sorted(filtered_sim_scores, key=lambda x:x[1], reverse=True)
    x = []
    for i in range(1, min(15, len(sorted_similar_review))):
        indx = sorted_similar_review[i][0]
        x.append([
            drug.iloc[indx, 0],
            drug.iloc[indx, 1],
            drug.iloc[indx, 2],
            drug.iloc[indx, 3],
            drug.iloc[indx, 4],
            drug.iloc[indx, 5]
        ])
    df = pd.DataFrame(x, columns=["Brand", "Contents", "Indications/Uses", "Dosage/Direction for Use", 
                                              "Contraindications", "Adverse Reactions"])
    return df


@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/recommendation", methods=["POST"])
def recommendation():
    if request.method == "POST":
        
        product_name = str(request.form["drugs"])
        df = recomendation_obat(product_name)
        headers = list(enumerate(df.columns, 1))
        rows = []

        drug = pickle.load(open('drug.pkl','rb'))
        indices = pd.Series(drug.index, index=drug['brand']).drop_duplicates()
        idx = indices[request.form["drugs"]]
        the_drugs = list(enumerate(drug.iloc[idx,:6], 1))

        for _, row in df.iterrows():
            rows.append(list(enumerate(row, 1)))

        return render_template("recommend.html", headers=headers, rows=rows, the_drugs=the_drugs)
    # else:
        # return render_template("Home.html")

if __name__ == '__main__':
    app.run(debug=True)
