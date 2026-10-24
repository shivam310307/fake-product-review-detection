# ReviewGuard AI - Dataset Documentation

## 1. Demonstration Dataset Schema

The bundled demonstration dataset (`dataset/sample_reviews.csv`) contains 1,600 labeled e-commerce reviews specifically structured for training and evaluating fake review classification algorithms.

| Column Name | Data Type | Description | Values / Examples |
| :--- | :--- | :--- | :--- |
| `category` | String | Product category domain | Electronics, Home & Kitchen, Sports & Outdoors, Beauty & Personal Care, Books & Media |
| `rating` | Integer | Star rating given with the review | 1, 2, 3, 4, 5 |
| `label` | String | Ground-truth class label | `genuine` (Original review), `fake` (Computer-generated/Manipulated) |
| `text` | String | Full review text body | Clean customer review text |
| `label_binary` | Integer | Normalized binary target | `0` = Genuine, `1` = Fake |
| `vocabulary_richness` | Float | Type-token ratio (unique words / total words) | Float between 0.00 and 1.00 |
| `average_word_length` | Float | Mean character length per word | Float (e.g. 4.82) |
| `sentence_count` | Integer | Number of sentences in review | Integer (e.g. 3) |
| `text_length` | Integer | Total character count of review text | Integer (e.g. 248) |

---

## 2. Label Convention & Standards

The application strictly adheres to the following binary labeling standards:
- **`0` = Genuine / Original Review (`OR`)**: Legitimate customer feedback reflecting authentic usage.
- **`1` = Fake / Computer-Generated Review (`CG`)**: Fabricated promotional praise or coordinated review-bombing attacks.

The system automatically detects alternative column names when user datasets are uploaded:
- **Review Text Columns Accepted:** `text`, `review`, `review_text`, `review_body`, `content`, `comments`
- **Label Columns Accepted:** `label`, `category`, `label_binary`, `target`, `class`, `deceptive`

---

## 3. Using Public Benchmark Datasets

For academic publications, final-year project viva demonstrations, and empirical research, you can upload real-world public datasets through the `/upload` dashboard:

1. **Ott et al. Deceptive Opinion Spam Dataset (Cornell University)**:
   - 1,600 hotel reviews (800 truthful, 800 deceptive generated via Mechanical Turk).
   - Standard benchmark in NLP fake review literature.
2. **Kaggle Amazon Fake Reviews Dataset**:
   - Contains ~40,000 labeled reviews across multiple product categories.
3. **Yelp Filtered Reviews Dataset**:
   - Reviews filtered by Yelp's proprietary recommendation algorithm vs recommended reviews.

*Academic Note: The bundled sample dataset is provided for immediate standalone demonstration without external dependencies. Real-world evaluation metrics reported in project reports should cite the specific empirical dataset utilized.*
