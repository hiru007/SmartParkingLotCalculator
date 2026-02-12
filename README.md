
# 🚗 Smart Parking Lot Rate Calculator

An extensible, SOLID-compliant rate engine built with Python 3.10+. This calculator evaluates multiple parking policies (Standard, Early Bird, Night Owl) and automatically applies the most cost-effective rate for the customer.

## 🛠 Features

* **Strategy Pattern:** Easily add new rate policies without modifying existing code.
* **Competitive Pricing:** Automatically selects the **minimum fee** among applicable policies.
* **Dynamic Scaling:** Supports multiple vehicle types (`CAR`, `BUS`, `MOTOR_CYCLE`) with specific multipliers.
* **Peak Hour Logic:** Granular 1.5x multiplier for weekday rush hours.
* **Loyalty Integration:** Tiered discounts for Silver, Gold, and Platinum members on flat-rate specials.

---

## 🚀 Getting Started

### Prerequisites

* [Docker](https://docs.docker.com/get-docker/) installed and running.
* A terminal/command prompt open in the project root.

### 1. Build the Docker Image

To package the application and its environment, run:

```bash
docker build -t parking-calc .

```

### 2. Run the Test Suite

The container is configured to run `unittest` discovery by default. This will verify all business use cases (Standard, Early Bird, Night Owl, and 24-hour guardrails).

```bash
docker run --rm parking-calc

```

---

## 🏗 Project Structure

* `app/interfaces.py`: Core abstractions and Enums (Vehicle types, Loyalty tiers).
* `app/policies/`: Individual strategy classes for each rate rule.
* `app/engine.py`: The logic coordinator that finds the best price.
* `tests/`: The `unittest` suite covering business requirements.




## 🏗️ Design Decisions & Assumptions

### 1. Calculation Protocol & Integrity

* **Rounding Rule:** All durations are rounded **upward** to the nearest full hour. For example, a stay of 61 minutes is treated as 2 hours for rate calculation.
* **Standard Policy Assessment:** Each hourly segment of a session is evaluated individually for peak-hour overlap. If any part of an hour (even one minute) falls within a peak window (7-10 AM or 4-7 PM Weekdays), the **1.5x multiplier** is applied specifically to that segment's base rate.
* **Financial Precision:** To ensure transactional integrity, all monetary comparisons in tests utilize `assertAlmostEqual`. 

### 2. Ambiguity Resolution (Critical Constraints)

* **The 24-Hour Disqualification:** To prevent abuse of flat-rate specials for multi-day stays, the system **invalidates all specials** (Early Bird and Night Owl) for any session  24 hours. These sessions revert to the **Standard Hourly Rate** exclusively.
* **Best Value Logic:** The engine performs an exhaustive evaluation of all valid policies for a given session. It automatically selects the **minimum derived amount**, ensuring the customer always receives the best possible rate.
* **Consecutive Day Rule:** The "Night Owl" policy strictly validates that the exit date is the calendar day immediately following the entry date. Stays ending on the same day as entry are ineligible.

### 3. Rate Compounding Order

The engine follows a specific order of operations to maintain mathematical consistency:

1. **Base Rate identification** (Standard) or **Flat Rate identification** (Specials).
2. **Loyalty Discount** application (calculated on the Flat Rate for Policies 2 & 3).
3. **Vehicle Multiplier** application (applied to the result of the previous step).
4. **Peak Surcharge** assessment (applied only to segments under the Standard Policy).

---

## 🧪 Testing Strategy

The test suite is organized into granular, explicit files to prioritize readability and simplify the verification of business rules.

* **`test_standard_policy.py`**: Validates progressive billing, individual peak-hour segment surcharges, the **24-hour stay fallback**, and the **Best Value** selection logic.
* **`test_early_bird_policy.py`**: Validates same-day window constraints, duration limits (15 hours), and vehicle/loyalty stacking.
* **`test_night_owl_policy.py`**: Verifies the "next-day" calendar transition, the 18-hour limit, and vehicle/loyalty stacking.

---

## 🤖 AI Interaction Transparency

* **Collaborative Refactoring:** AI was utilized to draft initial test patterns and calculation logic. These were manually refined to handle floating-point precision issues and complex peak-hour overlap logic.
* **Correction Cycle:** During development, a test failure regarding "5:59 AM entry" identified a gap in the fallback logic. The engine was corrected to ensure that when a Special Policy is disqualified, the Standard Policy correctly applies peak surcharges to every individual segment.

---

## 📖 Documentation & Prompt Engineering
This project was developed using a Meta-Prompting and TDD (Test-Driven Development) workflow.

AI Chat History: Detailed logs of the architectural decisions, context, and iterative development can be found in the docs/ai_chat_history.txt file.

Prompts: The specific Meta-Prompts used to generate the architecture and enforce SOLID principles are stored in the prompts/ directory for transparency and reproducibility.