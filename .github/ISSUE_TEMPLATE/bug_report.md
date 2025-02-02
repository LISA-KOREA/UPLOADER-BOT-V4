name: 🐛 Bug Report
description: Report a bug to help us improve.
title: "[Bug] "  # Pre-fills issue title with "[Bug] "
labels: ["bug"]
assignees: []

body:
  - type: markdown
    attributes:
      value: "## 🛠️ Bug Report\nThank you for taking the time to report an issue! Please fill out the details below."

  - type: textarea
    id: bug-description
    attributes:
      label: "🔍 Describe the bug"
      description: "Provide a clear and concise description of the issue."
      placeholder: "A brief summary of the bug..."
    validations:
      required: true

  - type: textarea
    id: reproduction-steps
    attributes:
      label: "📝 Steps to Reproduce"
      description: "List the steps to reproduce the issue."
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. Scroll down to '...'
        4. See the error...
    validations:
      required: true

  - type: textarea
    id: expected-behavior
    attributes:
      label: "✅ Expected Behavior"
      description: "Describe what you expected to happen instead."
      placeholder: "I expected it to..."
    validations:
      required: true

  - type: textarea
    id: actual-behavior
    attributes:
      label: "❌ Actual Behavior"
      description: "Describe what actually happened."
      placeholder: "Instead, this happened..."
    validations:
      required: true

  - type: input
    id: environment-desktop
    attributes:
      label: "💻 Desktop (if applicable)"
      description: "Provide details about your desktop environment."
      placeholder: "OS: Windows 11 | Browser: Chrome | Version: 115.0"

  - type: input
    id: environment-mobile
    attributes:
      label: "📱 Smartphone (if applicable)"
      description: "Provide details about your mobile environment."
      placeholder: "Device: iPhone 13 | OS: iOS 16 | Browser: Safari"

  - type: textarea
    id: screenshots
    attributes:
      label: "📷 Screenshots (if applicable)"
      description: "Attach screenshots to help explain the problem."
      placeholder: "Drag and drop or paste images here."

  - type: textarea
    id: additional-context
    attributes:
      label: "📝 Additional Context"
      description: "Any other relevant information about the issue?"
      placeholder: "Additional details..."
