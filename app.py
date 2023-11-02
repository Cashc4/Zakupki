import joblib
import streamlit as st
import pandas as pd

# Папка для сохранения фото
PHOTO_FOLDER = 'images/'
# Папка для сохранения моделей
MODELS_FOLDER = 'models/'

# Для загрузки модели
tf_idf = joblib.load(MODELS_FOLDER + 'tfidf_vectorizer.sav')
logreg = joblib.load(MODELS_FOLDER + 'logreg_model.sav')


def get_sample_with_all_groups(data):
    # Группируем данные по группе и выбираем одну случайную запись из каждой группы
    sample = data.groupby('Группа по ОКПД').sample(n=1).reset_index(drop=True)
    return sample


@st.cache_data
def load_data():
    return pd.read_csv('datasets/step_2.csv', nrows=10 ** 5)


data = load_data()

st.title("Анализ данных о закупках")
st.write(
    "Данный дашборд представляет анализ данных о государственных закупках. Ниже представлены различные визуализации "
    "данных, а также возможность получить прогноз для группы ОКПД по текстовому описанию закупки.")

# Отображение данных в виде таблицы
if st.checkbox("Показать случайные строки из данных"):
    sample_data = get_sample_with_all_groups(data)
    st.write(sample_data)

# Вывод сохраненных графиков
st.subheader("Распределение по группам ОКПД")
st.image(PHOTO_FOLDER + "Виды бюджета.jpeg", caption="Распределение контрактов по видам бюджета")

st.subheader("Топ контрагентов по количеству контрактов")
st.image(PHOTO_FOLDER + "Контрагенты.jpeg", caption="Топ контрагентов по количеству контрактов")

st.subheader("Распределение контрактов по регионам")
st.image(PHOTO_FOLDER + "Регионы.jpeg", caption="Распределение контрактов по регионам")

st.subheader("Распределение стоимости контрактов")
st.image(PHOTO_FOLDER + "Цены.jpeg", caption="Распределение стоимости контрактов")

st.subheader("Распределение срока выполнения контрактов")
st.image(PHOTO_FOLDER + "Сроки.jpeg", caption="Распределение срока выполнения контрактов")

st.subheader("Распределение контрактов по группам ОКПД")
st.image(PHOTO_FOLDER + "Группа ОКПД.jpeg", caption="Распределение контрактов по группам ОКПД")

st.subheader("Распределение контрактов по ОКПД-2")
st.image(PHOTO_FOLDER + "ОКПД-2.jpeg", caption="Распределение контрактов по ОКПД-2")

st.subheader("Частотное распределение слов в описании закупок")
st.image(PHOTO_FOLDER + "Частота.jpeg", caption="Частотное распределение слов")

st.subheader("Метрики качества классификации")
st.image(PHOTO_FOLDER + "logreg.png", caption="Метрики качества классификации для модели логистической регрессии")

# Прогнозирование (если вы хотите интегрировать модель прогнозирования)
st.subheader("Прогнозирование группы ОКПД")
user_input = st.text_input("Введите описание закупки:")
if user_input:
    X_test_tfidf = tf_idf.transform([user_input])
    y_pred = logreg.predict(X_test_tfidf[0])
    st.write(f"Предсказанная группа ОКПД: {y_pred[0]}")
