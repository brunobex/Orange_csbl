import os

from Orange.data import Table
from Orange.data.io import FileFormat
from Orange.widgets import gui
from Orange.widgets.utils.itemmodels import VariableListModel
from Orange.widgets.data.owselectcolumns import VariablesListItemView
from Orange.widgets.settings import Setting, ContextSetting, PerfectDomainContextHandler
from Orange.widgets.widget import OWWidget, Msg, Input, Output
from orangecontrib.text.corpus import Corpus, get_sample_corpora_dir
from orangecontrib.text.widgets.utils import widgets


class OWCorpus(OWWidget):
    name = "Teste"
    description = "Load a corpus of text documents."
    icon = "icons/TextFile.svg"
    priority = 100
    replaces = ["orangecontrib.text.widgets.owloadcorpus.OWLoadCorpus"]

    class Inputs:
        data = Input('Data', Table)

    class Outputs:
        corpus = Output('Corpus', Corpus)

    want_main_area = True
    resizing_enabled = True



    class Error(OWWidget.Error):
        read_file = Msg("Can't read file {} ({})")
        no_text_features_used = Msg("At least one text feature must be used.")
        corpus_without_text_features = Msg("Corpus doesn't have any textual features.")

    def __init__(self):
        super().__init__()

        self.corpus = None

    @Inputs.data
    def set_data(self, data):
        have_data = data is not None

        # Enable/Disable command when data from input
        self.file_widget.setEnabled(not have_data)
        self.browse_documentation.setEnabled(not have_data)

        if have_data:
            self.open_file(data=data)
        else:
            self.file_widget.reload()

    def open_file(self, path=None, data=None):
        self.closeContext()
        self.Error.clear()
        self.unused_attrs_model[:] = []
        self.used_attrs_model[:] = []
        if data:
            self.corpus = Corpus.from_table(data.domain, data)
        elif path:
            try:
                self.corpus = Corpus.from_file(path)
                self.corpus.name = os.path.splitext(os.path.basename(path))[0]
            except BaseException as err:
                self.Error.read_file(path, str(err))
        else:
            return

        self.update_info()
        self.used_attrs = list(self.corpus.text_features)
        if not self.corpus.text_features:
            self.Error.corpus_without_text_features()
            self.Outputs.corpus.send(None)
            return
        self.openContext(self.corpus)
        self.used_attrs_model.extend(self.used_attrs)
        self.unused_attrs_model.extend(
            [f for f in self.corpus.domain.metas
             if f.is_string and f not in self.used_attrs_model])

    def update_info(self):
        def describe(corpus):
            dom = corpus.domain
            text_feats = sum(m.is_string for m in dom.metas)
            other_feats = len(dom.attributes) + len(dom.metas) - text_feats
            text = \
                "{} document(s), {} text features(s), {} other feature(s).". \
                format(len(corpus), text_feats, other_feats)
            if dom.has_continuous_class:
                text += "<br/>Regression; numerical class."
            elif dom.has_discrete_class:
                text += "<br/>Classification; discrete class with {} values.". \
                    format(len(dom.class_var.values))
            elif corpus.domain.class_vars:
                text += "<br/>Multi-target; {} target variables.".format(
                    len(corpus.domain.class_vars))
            else:
                text += "<br/>Data has no target variable."
            text += "</p>"
            return text

        if self.corpus is None:
            self.info_label.setText("No corpus loaded.")
        else:
            self.info_label.setText(describe(self.corpus))


