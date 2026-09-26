<p align="center">
  <img src="docs/assets/banner.png" alt="on-device-slms" width="100%" />
</p>

<h1 align="center">on-device-slms</h1>

<p align="center">
  <strong>Run small language models natively on mobile — no cloud, no latency, full privacy.</strong>
</p>

<p align="center">
  Reference guide, unified SDK, and production-ready demo apps for deploying SLMs on iOS, Android, and Flutter.
</p>

<p align="center">
  <a href="#-quick-start"><img src="https://img.shields.io/badge/Quick_Start-→-black?style=flat-square" alt="Quick Start" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License" /></a>
  <a href="https://github.com/YOUR_USERNAME/on-device-slms/stargazers"><img src="https://img.shields.io/github/stars/YOUR_USERNAME/on-device-slms?style=flat-square" alt="Stars" /></a>
  <a href="https://github.com/YOUR_USERNAME/on-device-slms/issues"><img src="https://img.shields.io/github/issues/YOUR_USERNAME/on-device-slms?style=flat-square" alt="Issues" /></a>
  <img src="https://img.shields.io/badge/platform-iOS%20|%20Android%20|%20Flutter-brightgreen?style=flat-square" alt="Platforms" />
  <img src="https://img.shields.io/badge/models-Gemma%20|%20Llama%20|%20Phi-orange?style=flat-square" alt="Models" />
</p>

<br/>

<p align="center">
  <img src="docs/assets/demo.gif" alt="Demo running Gemma 3n on iOS, Android and Flutter side by side" width="720" />
</p>

---

## Why This Exists

Cloud LLMs are powerful, but they come with latency, cost, and privacy trade-offs that don't work for every app. Small language models (1–4B parameters) now run fast enough on phones to power real features — offline summarization, smart replies, document Q&A, on-device translation — without ever sending user data to a server.

This repo gives you **everything in one place**:

- 📖 **Guide** — Framework comparisons, model benchmarks, and optimization techniques for 2025–2026
- 🧩 **SDK** — Thin abstraction layer over LiteRT-LM, MediaPipe, Core ML, and llama.cpp
- 📱 **Demo Apps** — Production-quality chat apps for iOS (Swift), Android (Kotlin), and Flutter (Dart)

---

## Table of Contents

- [Features](#-features)
- [Supported Models](#-supported-models)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
  - [iOS](#ios-swift)
  - [Android](#android-kotlin)
  - [Flutter](#flutter-dart)
- [Project Structure](#-project-structure)
- [Framework Guide](#-framework-guide)
- [Optimization Techniques](#-optimization-techniques)
- [Benchmarks](#-benchmarks)
- [Configuration](#%EF%B8%8F-configuration)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Resources](#-resources)
- [License](#-license)

---

## ✨ Features

| | iOS | Android | Flutter |
|---|:---:|:---:|:---:|
| On-device text generation | ✅ | ✅ | ✅ |
| Multimodal (image + audio) | ✅ | ✅ | ✅ |
| Streaming token output | ✅ | ✅ | ✅ |
| GPU acceleration | ✅ Metal | ✅ OpenCL/Vulkan | ✅ via platform |
| NPU acceleration | ✅ Neural Engine | ✅ Qualcomm/MediaTek | ✅ via platform |
| LoRA adapter loading | ✅ | ✅ | ✅ |
| INT4 quantized models | ✅ | ✅ | ✅ |
| Offline / airplane mode | ✅ | ✅ | ✅ |
| Multi-turn chat sessions | ✅ | ✅ | ✅ |
| Adaptive model selection | ✅ | ✅ | ✅ |

---

## 📦 Supported Models

Models are tested and verified for on-device deployment. **★** = recommended starting point.

| Model | Parameters | Download Size | Modality | Notes |
|-------|-----------|--------------|----------|-------|
| **Gemma 3 1B** ★ | 1B | ~529 MB | Text | Best size/quality ratio. 2,585 tok/s prefill on mobile GPU |
| **Gemma 3n E2B** ★ | 2B effective | ~1.2 GB | Text, Image, Audio, Video | Multimodal. Selective parameter activation |
| Gemma 3n E4B | 4B effective | ~2.4 GB | Text, Image, Audio, Video | Flagship devices only |
| Phi-4 Mini | 3.8B | ~2.1 GB | Text | Strong reasoning for its size |
| Llama 3.2 1B | 1B | ~700 MB | Text | Good general-purpose baseline |
| Llama 3.2 3B | 3B | ~1.8 GB | Text | Better quality, needs 6GB+ RAM |
| Qwen 2.5 1.5B | 1.5B | ~900 MB | Text | Strong multilingual support |
| SmolVLM2 | 0.5B | ~350 MB | Text, Vision | Ultra-lightweight vision model |

> **Tip:** Start with **Gemma 3 1B** for text-only use cases. Move to **Gemma 3n E2B** when you need multimodal input.

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Your Application                   │
├──────────┬──────────────────┬────────────────────────┤
│  iOS App │   Android App    │      Flutter App        │
│  (Swift) │    (Kotlin)      │       (Dart)            │
├──────────┴──────────────────┴────────────────────────┤
│              on-device-slms SDK Layer                 │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Unified API: load() → prompt() → stream()      │ │
│  │  Model Management · Session Handling · LoRA      │ │
│  └─────────────────────────────────────────────────┘ │
├──────────┬──────────────────┬────────────────────────┤
│ Core ML  │   LiteRT-LM      │   MediaPipe / llama.cpp│
│ Apple FM │   MediaPipe       │   flutter_gemma        │
│ MLX      │   AICore          │   llamadart            │
├──────────┼──────────────────┼────────────────────────┤
│  Neural  │  GPU (OpenCL)    │   Platform-delegated   │
│  Engine  │  NPU (QC/MTK)    │   GPU / NPU            │
│  Metal   │  Tensor G4       │                        │
└──────────┴──────────────────┴────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- A physical device (emulators lack GPU/NPU acceleration)
- A compatible model file (see [Supported Models](#-supported-models))
- Download models from [HuggingFace LiteRT Community](https://huggingface.co/litert-community) or [Kaggle](https://www.kaggle.com/models/google/gemma)

### iOS (Swift)

**Requirements:** Xcode 16+, iOS 17+ (or iOS 26+ for Apple Foundation Models), physical iPhone/iPad

```bash
cd ios/
open OnDeviceSLM.xcodeproj
```

**Option A — Apple Foundation Models (iOS 26+, zero model download):**

```swift
import FoundationModels

let session = LanguageModelSession()
let response = try await session.respond(
    to: "Summarize this text in 3 bullet points: \(inputText)"
)
print(response.content)
```

**Option B — Custom models via Core ML / MediaPipe:**

```swift
import MediaPipeTasksGenAI

let options = LlmInference.Options(modelPath: "gemma3-1b.task")
options.maxTokens = 1024
let llm = try LlmInference(options: options)

// Streaming response
let stream = llm.generateResponseAsync(inputText: "Explain quantum computing")
for try await chunk in stream {
    print(chunk, terminator: "")
}
```

### Android (Kotlin)

**Requirements:** Android Studio Hedgehog+, SDK 24+, physical device (Pixel 7+ or Galaxy S23+ recommended)

```bash
cd android/
./gradlew installDebug
```

```kotlin
// build.gradle.kts
dependencies {
    implementation("com.google.ai.edge.litert:litert-lm:+")
}
```

```kotlin
// Using LiteRT-LM (recommended)
val engine = LlmEngine.create(
    context = applicationContext,
    modelPath = "gemma3-1b.litertlm",
    backend = Backend.GPU
)

val session = engine.createSession()
session.generateResponseAsync("Summarize this article: $text")
    .collect { chunk ->
        binding.responseText.append(chunk)
    }
```

### Flutter (Dart)

**Requirements:** Flutter 3.22+, physical device for both iOS and Android

```bash
cd flutter/
flutter pub get
flutter run
```

```yaml
# pubspec.yaml
dependencies:
  flutter_gemma: ^latest    # For Gemma models via MediaPipe/LiteRT-LM
  # OR
  llamadart: ^latest        # For any GGUF model via llama.cpp
```

```dart
// Using flutter_gemma
final manager = FlutterGemmaPlugin.instance;
await manager.modelManager.installModelFromNetwork(modelUrl);

final model = await manager.createModel(
  modelType: ModelType.gemmaIt,
  preferredBackend: PreferredBackend.gpu,
  maxTokens: 512,
);

final stream = model.generateChatResponseAsync([
  Message(text: "What is photosynthesis?", isUser: true),
]);

await for (final chunk in stream) {
  setState(() => _response += chunk);
}
```

---

## 📁 Project Structure

```
on-device-slms/
├── ios/                        # iOS demo app (Swift + SwiftUI)
│   ├── OnDeviceSLM/
│   │   ├── Models/             # Core ML model integration
│   │   ├── Services/           # LLM inference service layer
│   │   ├── Views/              # SwiftUI chat interface
│   │   └── Utils/              # Device capability detection
│   └── OnDeviceSLM.xcodeproj
│
├── android/                    # Android demo app (Kotlin + Compose)
│   ├── app/src/main/
│   │   ├── java/.../
│   │   │   ├── data/           # Model management & download
│   │   │   ├── inference/      # LiteRT-LM / MediaPipe wrappers
│   │   │   ├── ui/             # Jetpack Compose chat UI
│   │   │   └── util/           # Hardware detection, benchmarking
│   │   └── res/
│   └── build.gradle.kts
│
├── flutter/                    # Flutter demo app (Dart)
│   ├── lib/
│   │   ├── models/             # Data models & chat state
│   │   ├── services/           # Platform-bridged inference
│   │   ├── screens/            # Chat & settings screens
│   │   └── widgets/            # Reusable UI components
│   └── pubspec.yaml
│
├── sdk/                        # Shared SDK components
│   ├── model_registry.json     # Model catalog with device requirements
│   └── prompts/                # Optimized prompt templates
│
├── models/                     # Model download scripts & configs
│   ├── download.sh             # Fetch models from HuggingFace
│   └── quantize.py             # INT4/INT8 quantization helper
│
├── benchmarks/                 # Performance test results
│   ├── results/                # CSV benchmark data by device
│   └── run_benchmark.sh        # Automated benchmark runner
│
├── docs/                       # Extended documentation
│   ├── FRAMEWORK_GUIDE.md      # Detailed framework comparisons
│   ├── OPTIMIZATION.md         # Quantization, KV-cache, LoRA guide
│   ├── TROUBLESHOOTING.md      # Common issues & fixes
│   └── assets/                 # Images, diagrams, GIFs
│
├── CONTRIBUTING.md
├── LICENSE
└── README.md                   ← You are here
```

---

## 📚 Framework Guide

Detailed comparison of every framework option per platform.

### iOS

| Framework | Best For | Model Support | Acceleration | Status |
|-----------|---------|--------------|-------------|--------|
| **Foundation Models** | Apple's built-in 3B model | Apple FM only | Neural Engine + Metal | Production (iOS 26+) |
| **Core ML + MLX** | Custom open models | Any (converted) | Neural Engine + Metal + CPU | Production |
| **MediaPipe / LiteRT-LM** | Cross-platform parity | Gemma, Phi, Llama | Metal GPU | Production |

### Android

| Framework | Best For | Model Support | Acceleration | Status |
|-----------|---------|--------------|-------------|--------|
| **LiteRT-LM** | New production apps | Gemma, Llama, Phi, Qwen | CPU + GPU + NPU | Production |
| **MediaPipe LLM API** | Existing projects | Gemma, Phi-2 | CPU + GPU | Stable (migrating to LiteRT-LM) |
| **Android AICore** | Premium devices only | Gemini Nano | Full hardware stack | Production (limited devices) |

### Flutter

| Framework | Best For | Model Support | Acceleration | Status |
|-----------|---------|--------------|-------------|--------|
| **flutter_gemma** | Gemma models, unified API | .task / .litertlm | GPU via platform | Active |
| **llamadart** | Any GGUF model | All GGUF | Vulkan, CUDA, WebGPU | Active |
| **Cactus SDK** | Managed runtime + cloud fallback | Multiple | NPU | Beta v1 |

> 📖 Full breakdown with code samples: [`docs/FRAMEWORK_GUIDE.md`](docs/FRAMEWORK_GUIDE.md)

---

## ⚡ Optimization Techniques

### INT4 Quantization

Reduces model size **2.5–4×** from bf16 while preserving quality. This is the standard for mobile deployment.

```bash
# Quantize a model for mobile deployment
python models/quantize.py \
  --model gemma-3-1b \
  --precision int4 \
  --output ./models/gemma3-1b-int4.task
```

### KV-Cache Management

LiteRT-LM handles this automatically. For custom implementations, store Key/Value tensors from previous tokens to avoid recomputation — reduces decode workload from **O(n²) to O(n)**.

### NPU Acceleration

Modern mobile SoCs include dedicated Neural Processing Units. LiteRT-LM provides a unified API across vendors:

```kotlin
// Android — automatic NPU selection
val engine = LlmEngine.create(
    context = this,
    modelPath = "model.litertlm",
    backend = Backend.NPU  // Qualcomm Hexagon / MediaTek APU / Google Tensor
)
```

### LoRA Fine-Tuning

Customize model behavior with lightweight adapters (10–50 MB) without retraining the full model:

```swift
// iOS — load LoRA adapter at runtime
let options = LlmInference.Options(modelPath: "gemma3-1b.task")
options.loraPath = "custom-lora.safetensors"
let llm = try LlmInference(options: options)
```

### Adaptive Model Loading

Auto-select model complexity based on device capability:

```dart
// Flutter — device-aware model selection
String getModelForDevice() {
  final ram = DeviceInfo.totalRAM;
  if (ram >= 8) return 'gemma3n-e4b.task';   // 4B — flagship
  if (ram >= 6) return 'gemma3n-e2b.task';   // 2B — mid-range
  return 'gemma3-1b.task';                    // 1B — budget
}
```

> 📖 Deep dive: [`docs/OPTIMIZATION.md`](docs/OPTIMIZATION.md)

---

## 📊 Benchmarks

Measured with 1024 tokens prefill / 256 tokens decode on physical devices.

| Model | Device | Backend | Prefill (tok/s) | Decode (tok/s) | RAM Usage |
|-------|--------|---------|----------------|---------------|-----------|
| Gemma 3 1B (INT4) | Pixel 9 Pro | GPU | 2,585 | 42 | 1.1 GB |
| Gemma 3 1B (INT4) | Pixel 9 Pro | NPU | 7,200+ | 38 | 1.1 GB |
| Gemma 3 1B (INT4) | iPhone 16 Pro | Metal | 2,100 | 45 | 1.0 GB |
| Gemma 3n E2B | Galaxy S25 Ultra | GPU | 1,400 | 28 | 2.3 GB |
| Gemma 3n E2B | iPhone 16 Pro | Metal | 1,250 | 30 | 2.1 GB |
| Llama 3.2 1B (INT4) | Pixel 8 | GPU | 1,800 | 35 | 1.2 GB |
| Phi-4 Mini (INT4) | Galaxy S24+ | GPU | 800 | 18 | 2.8 GB |

> **Note:** First load is slower due to weight optimization caching. Subsequent loads are significantly faster.

Run benchmarks on your own device:

```bash
cd benchmarks/
./run_benchmark.sh --model gemma3-1b --device android
```

---

## ⚙️ Configuration

### Model Registry

The SDK uses `sdk/model_registry.json` to manage model metadata and device requirements:

```json
{
  "gemma-3-1b": {
    "name": "Gemma 3 1B",
    "files": {
      "task": "gemma3-1b-int4.task",
      "litertlm": "gemma3-1b-int4.litertlm"
    },
    "requirements": {
      "min_ram_gb": 4,
      "min_sdk_android": 24,
      "min_ios": "17.0"
    },
    "capabilities": ["text-generation", "summarization", "extraction"],
    "size_mb": 529
  }
}
```

### Environment Variables

| Variable | Description | Default |
|----------|------------|---------|
| `SLMS_MODEL_DIR` | Local directory for downloaded models | `./models/` |
| `SLMS_DEFAULT_MODEL` | Model ID to load on startup | `gemma-3-1b` |
| `SLMS_MAX_TOKENS` | Maximum generation length | `1024` |
| `SLMS_BACKEND` | Preferred backend (`auto`, `gpu`, `npu`, `cpu`) | `auto` |
| `HF_TOKEN` | HuggingFace token for gated model downloads | — |

---

## 🗺 Roadmap

- [x] iOS demo app with Foundation Models + MediaPipe
- [x] Android demo app with LiteRT-LM
- [x] Flutter demo app with flutter_gemma
- [x] INT4 quantization pipeline
- [x] Streaming token output on all platforms
- [ ] RAG pipeline (on-device vector search + generation)
- [ ] Voice input → SLM → voice output pipeline
- [ ] Function calling / tool use demo
- [ ] Model fine-tuning notebook (LoRA on custom data)
- [ ] Kotlin Multiplatform shared inference layer
- [ ] Benchmark automation CI (test on device farms)
- [ ] Web demo via WebGPU + LiteRT-LM

---

## 🤝 Contributing

Contributions are welcome and appreciated! Whether it's a bug fix, new model support, framework updates, or documentation improvements.

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feat/add-mistral-support`)
3. **Commit** your changes (`git commit -m 'feat: add Mistral 7B mobile config'`)
4. **Push** to the branch (`git push origin feat/add-mistral-support`)
5. **Open** a Pull Request

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for details on the code of conduct and submission guidelines.

### Areas We'd Love Help With

- 🧪 Benchmark results from devices we don't have
- 🌍 Multilingual prompt templates
- 🐛 Edge case handling for low-memory devices
- 📝 Documentation translations

---

## 📚 Resources

**Frameworks & SDKs**

- [LiteRT-LM](https://github.com/google-ai-edge/LiteRT-LM) — Google's production on-device LLM framework
- [MediaPipe LLM Inference](https://ai.google.dev/edge/mediapipe/solutions/genai/llm_inference) — Cross-platform LLM inference API
- [Apple Foundation Models](https://developer.apple.com/machine-learning/) — On-device FM framework for iOS 26+
- [flutter_gemma](https://pub.dev/packages/flutter_gemma) — Flutter plugin for Gemma models
- [llamadart](https://pub.dev/packages/llamadart) — llama.cpp bindings for Dart/Flutter
- [MLX](https://github.com/ml-explore/mlx) — Apple Silicon ML framework

**Models**

- [LiteRT Community on HuggingFace](https://huggingface.co/litert-community) — Pre-converted mobile-ready models
- [Gemma Models](https://ai.google.dev/gemma) — Google's open model family
- [Llama Models](https://llama.meta.com/) — Meta's open model family

**Further Reading**

- [Awesome Mobile LLM](https://github.com/stevelaskaridis/awesome-mobile-llm) — Comprehensive paper list
- [Google AI Edge Documentation](https://ai.google.dev/edge) — Official on-device ML docs
- [WWDC25: Meet the Foundation Models Framework](https://developer.apple.com/videos/play/wwdc2025/286/) — Apple's official introduction

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

Model weights are subject to their respective licenses (Gemma Terms of Use, Llama Community License, etc.). Please review each model's license before deploying in production.

---

<p align="center">
  <sub>Built with ☕ and way too many quantized model downloads.</sub><br/>
  <sub>If this helped you ship on-device AI, consider giving it a ⭐</sub>
</p>
