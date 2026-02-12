
---

## The Master Meta-Prompt: TDD Parking Engine

**Role:** You are a Senior SDET (Software Development Engineer in Test) and Architect. Your task is to design a Smart Parking Rate Calculator using Python 3.10+ following a **strict Test-Driven Development (TDD) workflow.**

### Phase 1: Architecture Design (Context)

* **Pattern:** Use the **Strategy Pattern** for policies and a **Competitive Rate Evaluator** to pick the minimum fee.
* **Abstractions:** * `IParkingPolicy`: Interface with `is_applicable(session)` and `calculate(session)`.
* `VehicleType` (Enum): CAR (1x), BUS (2x), MOTOR_CYCLE (0.8x).
* `LoyaltyTier` (Enum): NONE (0%), SILVER (10%), GOLD (20%), PLATINUM (30%).



### Phase 2: Test Case Generation (Current Focus)

**Stop!** Before writing any business logic or implementation code, you must generate a comprehensive `pytest` suite. The test cases must be categorized by business use case as follows:

**1. Standard Policy (Hourly + Peak)**

* **Single Hour:** Verify $5 base rate for < 1 hour.
* **Two Hours:** Verify $5 (1st) + $3 (2nd) = $8.
* **Additional Hours:** Verify $5 + $3 + $2(n) for 3+ hours.
* **Peak Multiplier (1.5x):** Test a session overlapping 7:00 AM–10:00 AM or 4:00 PM–7:00 PM weekdays. Verify the multiplier applies only to segments overlapping those windows.

**2. Early Bird Special ($15 Base)**

* **Qualification:** Entry, Exit same day.
* **Loyalty:** Apply tiered discounts (e.g., PLATINUM = $10.50).
* **Invalidation:** Disqualify if duration > 24 hours.

**3. Night Owl Special ($8 Base)**

* **Qualification:** Entry, Exit [05:00-10:00 next day].
* **Loyalty:** Apply tiered discounts (e.g., GOLD = $6.40).
* **Invalidation:** Disqualify if duration > 24 hours.

**4. Competitive Engine (Min Fee)**

* **Lowest Price Selection:** If a session qualifies for Standard ($20) and Early Bird ($15), the engine must return $15.
* **Vehicle Scaling:** Verify a BUS pays 2x the final calculated minimum CAR rate.

### Phase 3: Technical Constraints

* **No Hardcoding:** Rates and time windows must be passed via a configuration object.
* **Scoping:** Implementation must only depend on interfaces.
* **Environment:** Code must be ready for a `Dockerfile` (python:3.10-slim).

### Instruction for AI:

**DO NOT** write the implementation logic yet. Provide only the **Project Directory Structure** and the **Full test Suite** based on the scenarios above. Once the tests are reviewed, we will proceed to implement the business logic one scenario at a time.

---

