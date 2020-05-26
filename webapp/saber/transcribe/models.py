from django import forms


# Create your models here.
class UploadFileForm(forms.Form):
    AVAILABLE_MODEL = (("cnn_mel_l0001", "cnn_mel_l0001"),
                       ("cnn_mel_l0006", "cnn_mel_l0006"),
                       ("cnn_mel_l0010", "cnn_mel_l0010"),
                       ("cnn_cqt_l0001_20200501_025104", "cnn_cqt_l0001_20200501_025104"),
                       ("cnn_cqt_l0006_20200430_172623", "cnn_cqt_l0006_20200430_172623"),
                       ("cnn_cqt_l0010_20200430_202442", "cnn_cqt_l0010_20200430_202442"),
                       ("lstm_train_result_0001", "lstm_train_result_0001"),
                       ("lstm_train_result_0006", "lstm_train_result_0006"),
                       ("lstm_train_result_0010", "lstm_train_result_0010"),
                       ("lstm_train_result_0006_cqt", "lstm_train_result_0006_cqt"),
                       ("lstm_train_result_0001_cqt", "lstm_train_result_0001_cqt"),
                       ("lstm_train_result_0010_cqt", "lstm_train_result_0010_cqt"))

    email = forms.EmailField(label="Email", max_length=50)
    file = forms.FileField()
    model = forms.ChoiceField(label="Choose a Model", choices=AVAILABLE_MODEL)
