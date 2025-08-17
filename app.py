from flask import Flask, render_template, request
from Bio.SeqUtils import molecular_weight
from Bio.Seq import Seq
from collections import Counter

app = Flask(__name__)

# Function to calculate amino acid composition
def calculate_aa_composition(sequence):
    aa_count = Counter(sequence)
    total_length = len(sequence)
    aa_percent = {aa: (count / total_length) * 100 for aa, count in aa_count.items()}
    return aa_count, aa_percent

# Custom function for pI calculation
def calculate_pI(sequence):
    pKa_values = {
        'A': 2.34, 'C': 1.96, 'D': 3.90, 'E': 4.07, 'F': 3.30,
        'G': 2.34, 'H': 7.59, 'I': 2.36, 'K': 9.60, 'L': 2.36,
        'M': 2.28, 'N': 3.10, 'P': 2.00, 'Q': 3.50, 'R': 12.48,
        'S': 2.21, 'T': 2.23, 'V': 2.32, 'W': 3.40, 'Y': 10.07
    }

    aa_count = Counter(sequence)
    pI = 7  # Initial guess for the pI
    for aa, count in aa_count.items():
        if aa in pKa_values:
            pI += pKa_values[aa] * count

    return round(pI / len(sequence), 2)


# Route for sequence input and result calculation
@app.route('/sequence', methods=['GET', 'POST'])
def sequence():
    if request.method == 'POST':
        sequence = request.form['sequence']
        seq_obj = Seq(sequence)

        # Calculate various properties
        mw = molecular_weight(seq_obj)
        pI = calculate_pI(sequence)
        aa_count, aa_percent = calculate_aa_composition(sequence)

        # Atomic composition (simplified for the example)
        atomic_composition = {
            'C': 84, 'H': 134, 'N': 28, 'O': 33, 'S': 4
        }

        # Extinction Coefficients (simplified example)
        extinction_coeff = {
            'cysteine_reduced': 1490, 'cysteine_oxidized': 1740
        }

        # Estimated half-life
        half_life = {
            'mammalian': '4.4 hours',
            'yeast': '>20 hours',
            'E_coli': '>10 hours'
        }

        # Instability index and other properties
        instability_index = 26.40
        aliphatic_index = 39.29
        GRAVY = 0.814

        return render_template('sequence_input.html', sequence=sequence, mw=mw, pI=pI, aa_count=aa_count,
                               aa_percent=aa_percent, atomic_composition=atomic_composition,
                               extinction_coeff=extinction_coeff, half_life=half_life, instability_index=instability_index,
                               aliphatic_index=aliphatic_index, GRAVY=GRAVY)

    return render_template('sequence_input.html')

# Only ONE welcome route function allowed
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/structure')
def structure_viewer():
    return render_template('structure_viewer.html')


if __name__ == '__main__':
    app.run(debug=True)
