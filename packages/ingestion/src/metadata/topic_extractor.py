# Maps surface forms (Spanish & English) → canonical topic name.
# When a surface form is found in the text, the canonical name is emitted.
KEYWORD_MAP = {
    # Neural networks
    "neural network": "neural_network",
    "red neuronal": "neural_network",
    "redes neuronales": "neural_network",
    # Convolutional networks
    "convolutional neural network": "cnn",
    "convolutional": "cnn",
    "convolucional": "cnn",
    "convolucionales": "cnn",
    "conv2d": "cnn",
    # Recurrent networks
    "recurrent neural network": "rnn",
    "red recurrente": "rnn",
    "redes recurrentes": "rnn",
    "lstm": "rnn",
    "gru": "rnn",
    # Transformer / Attention
    "transformer": "transformer",
    "attention": "attention",
    "atención": "attention",
    "self-attention": "attention",
    # Training
    "overfitting": "overfitting",
    "sobreajuste": "overfitting",
    "regularization": "regularization",
    "regularización": "regularization",
    "weight decay": "regularization",
    "dropout": "dropout",
    "batch normalization": "batch_normalization",
    "batch norm": "batch_normalization",
    "early stopping": "early_stopping",
    "data augmentation": "data_augmentation",
    "aumento de datos": "data_augmentation",
    # Optimization
    "gradient descent": "gradient_descent",
    "descenso de gradiente": "gradient_descent",
    "descenso del gradiente": "gradient_descent",
    "backpropagation": "backpropagation",
    "retropropagación": "backpropagation",
    "loss function": "loss_function",
    "función de pérdida": "loss_function",
    "función de loss": "loss_function",
    "activation function": "activation_function",
    "función de activación": "activation_function",
    "relu": "activation_function",
    "sigmoid": "activation_function",
    "softmax": "activation_function",
    "learning rate": "learning_rate",
    "tasa de aprendizaje": "learning_rate",
    "momentum": "momentum",
    "optimizer": "optimizer",
    "optimizador": "optimizer",
    "adam": "optimizer",
    "sgd": "optimizer",
    # Transfer learning
    "transfer learning": "transfer_learning",
    "fine-tuning": "fine_tuning",
    "fine tuning": "fine_tuning",
    # Deep / Machine learning
    "deep learning": "deep_learning",
    "aprendizaje profundo": "deep_learning",
    "machine learning": "machine_learning",
    "aprendizaje automático": "machine_learning",
    "aprendizaje de máquina": "machine_learning",
    # Task types
    "supervised learning": "supervised_learning",
    "aprendizaje supervisado": "supervised_learning",
    "unsupervised learning": "unsupervised_learning",
    "aprendizaje no supervisado": "unsupervised_learning",
    "reinforcement learning": "reinforcement_learning",
    "aprendizaje por refuerzo": "reinforcement_learning",
    # Vision / NLP
    "computer vision": "computer_vision",
    "visión computacional": "computer_vision",
    "visión por computador": "computer_vision",
    "natural language processing": "nlp",
    "procesamiento de lenguaje natural": "nlp",
    # Common layers / concepts
    "pooling": "pooling",
    "max pooling": "pooling",
    "max pool": "pooling",
    "fully connected": "fully_connected",
    "dense": "fully_connected",
    "flatten": "flatten",
    "embedding": "embedding",
    "clasificación": "classification",
    "classification": "classification",
    "regression": "regression",
    "regresión": "regression",
    # GAN / VAE
    "generative adversarial network": "gan",
    "gan": "gan",
    "variational autoencoder": "vae",
    "autoencoder": "autoencoder",
    # Specific architectures
    "alexnet": "alexnet",
    "resnet": "resnet",
    "vgg": "vgg",
}


def extract_topics(text: str) -> list[str]:
    text_lower = text.lower()
    topics = set()
    for surface_form, canonical in KEYWORD_MAP.items():
        if surface_form in text_lower:
            topics.add(canonical)
    return sorted(topics)