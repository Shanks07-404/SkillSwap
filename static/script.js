document.addEventListener("DOMContentLoaded", () => {
    // Core Layout Hook Elements
    const runQueryBtn = document.getElementById("run-query-btn");
    const skillInput = document.getElementById("skill-input");
    const matrixOutput = document.getElementById("matrix-output");

    // Modal System Control Hook Elements
    const swapModal = document.getElementById("swap-modal");
    const modalTargetUser = document.getElementById("modal-target-user");
    const modalHoursInput = document.getElementById("modal-hours-input");
    const modalCancelBtn = document.getElementById("modal-cancel-btn");
    const modalConfirmBtn = document.getElementById("modal-confirm-btn");

    let activeTargetNode = null; // Holds the runtime target data object for the transaction context

    // FUNCTION: Execute the Skill Matrix Database Query
    async function runMatchingQuery() {
        const skillName = skillInput.value.trim();
        if (!skillName) {
            matrixOutput.innerHTML = `<span class="error-text">Please type a valid skill descriptor.</span>`;
            return;
        }

        matrixOutput.innerHTML = "Executing relational matching array pipeline...";

        try {
            // FastAPI endpoint execution
            const response = await fetch(`/api/matching/search?skill=${encodeURIComponent(skillName)}`);
            
            if (!response.ok) {
                matrixOutput.innerHTML = `<span class="error-text">Backend returned status ${response.status}. Check terminal logs!</span>`;
                return;
            }

            const data = await response.json();
            
            // Explicitly handle empty data arrays cleanly without throwing a catch error
            if (!data || data.length === 0) {
                matrixOutput.innerHTML = `<div style="color: #FF2A85; font-weight: 700; padding: 5px;">⚠️ No active members found matching the criteria for "${skillName}".</div>`;
                return;
            }

            // Render matching records visually as styled sub-cards matching your exact brutalist UI layout template
            matrixOutput.innerHTML = "";
            data.forEach(match => {
                const card = document.createElement("div");
                card.className = "matrix-card";
                
                // Construct the block layout frame, aligning the Select call-to-action button squarely to the right
                card.innerHTML = `
                    <div style="border: 2px solid #000; background: #fff; padding: 20px; margin-bottom: 15px; box-shadow: 4px 4px 0px #000; border-radius: 0px; display: flex; justify-content: space-between; align-items: center; text-align: left;">
                        <div>
                            <h4 style="margin: 0 0 8px 0; font-size: 1.2rem; font-weight: 900; color: #FF2A85;">⚡ MATCH FOUND: ${match.user_name || 'Anonymous User'}</h4>
                            <p style="margin: 0; font-size: 1rem; color: #000; font-family: sans-serif;">
                                <strong>Skill Level:</strong> ${match.level || 'Intermediate'} | <strong>Availability:</strong> ${match.availability || 'Flexible'}
                            </p>
                        </div>
                        <button class="select-member-btn" data-username="${match.user_name}" data-expert-id="${match.expert_id}" style="background: #FFF59D; color: #000; border: 3px solid #000; font-weight: 900; padding: 10px 20px; cursor: pointer; box-shadow: 3px 3px 0px #000; font-size: 1rem; transition: transform 0.1s;">
                            SELECT
                        </button>
                    </div>
                `;
                matrixOutput.appendChild(card);
            });

            // Bind click event handlers to the generated select buttons on the fly
            document.querySelectorAll(".select-member-btn").forEach(button => {
                button.addEventListener("click", (e) => {
                    // Cache target data attributes directly from the targeted button component
                    activeTargetNode = {
                        id: e.target.getAttribute("data-expert-id"),
                        name: e.target.getAttribute("data-username")
                    };
                    
                    // Hydrate modal fields and trigger structural modal pop-up display wrapper array
                    modalTargetUser.innerText = `★ ${activeTargetNode.name} (Node ID: ${activeTargetNode.id})`;
                    modalHoursInput.value = "1";
                    swapModal.style.display = "flex";
                });
            });

        } catch (error) {
            // Exposes the real JS runtime or network breakdown description inside your console card
            matrixOutput.innerHTML = `<span class="error-text">JS Exception: ${error.message}</span>`;
        }
    }

    // Modal Cancellation Trigger Controls
    modalCancelBtn.addEventListener("click", () => {
        swapModal.style.display = "none";
        activeTargetNode = null;
    });

    // Modal Confirmation Execution Sequence Process Pipeline
    modalConfirmBtn.addEventListener("click", async () => {
        if (!activeTargetNode) return;
        
        const requestedHours = parseInt(modalHoursInput.value);
        if (isNaN(requestedHours) || requestedHours < 1) {
            alert("Please enter a valid hour allocation block volume count.");
            return;
        }

        try {
            // Dispatch request directly to the freshly instantiated FastAPI router pipeline mapping receiver
            const response = await fetch('/api/transaction/allocate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    target_user_id: parseInt(activeTargetNode.id),
                    hours_allocated: requestedHours
                })
            });

            const result = await response.json();

            if (response.ok) {
                alert(`Allocation Success!\n${result.detail}`);
                swapModal.style.display = "none";
                activeTargetNode = null;
                runMatchingQuery(); // Instantly fire secondary query scan to sync the local console layer
            } else {
                alert(`Transaction Rejected by Ledger Engine: ${result.detail}`);
            }
        } catch (error) {
            alert(`Network synchronization failure error: ${error.message}`);
        }
    });

    // Wire up listeners to design buttons
    runQueryBtn.addEventListener("click", runMatchingQuery);
});