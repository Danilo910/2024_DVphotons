import matplotlib.pyplot as plt

# Create a figure for displaying equations
fig, ax = plt.subplots(figsize=(8, 10))
ax.axis('off')  # Hide axes

# Display equations as LaTeX text (replace \text{} with \mathrm{} for compatibility)
equations = [
    r"$\Gamma(h \to \phi \phi) = \frac{1}{2!} \frac{|\lambda_{h\phi}|^2 P_0}{8 \pi m_h^2}$",
    r"In natural units:",
    r"$\Gamma(h \to \phi \phi) = \frac{1}{2!} \frac{|\lambda_{h\phi}|^2 P_0}{8 \pi m_h^2}$",
    r"$P_0 = \frac{1}{2 m_h} \sqrt{m_h^4 + 2 m_h^2 m_\phi^2 - 2 m_h^2 m_\phi^2 - 2 m_h^2 m_\phi^2 - 2 m_\phi^4}$",
    r"$P_0 = \frac{1}{2 m_h} \sqrt{m_h^4 - 4 M^2 m_\phi^2}$",
    r"$P_0 = \frac{1}{2 m_h} \sqrt{m_h^2 (m_h^2 - 4 m_\phi^2)}$",
    r"$P_0 = \frac{1}{2} \sqrt{m_h^2 - 4 m_\phi^2}$",
    r"Thus, the decay width becomes:",
    r"$\Gamma(h \to \phi \phi) = \frac{1}{2!} \frac{|\lambda_{h\phi}|^2 \sqrt{m_h^2 - 4 m_\phi^2}}{8 \pi m_h}$",
    r"Branching Ratio Constraints:",
    r"$\mathrm{BR}(h \to \phi \phi) = \frac{f(m_h, m_\phi) \lambda_{h\phi}^2}{f \lambda_{h\phi}^2 + \Gamma_{\mathrm{SM}}}$",
    r"$f(m_h, m_\phi) = \frac{\sqrt{m_h^2 - 4 m_\phi^2}}{8 \pi m_h}$",
    r"Rearranging:",
    r"$(f \lambda^2 + \Gamma_{\mathrm{SM}}) \mathrm{BR} = f \lambda^2$",
    r"$\mathrm{BR} f \lambda^2 + \Gamma_{\mathrm{SM}} \mathrm{BR} - f \lambda^2 = 0$",
    r"$\lambda^2 = \frac{\Gamma_{\mathrm{SM}} \mathrm{BR}}{f(1 - \mathrm{BR})}$",
    r"Maximum constraint on $\lambda$:",
    r"$\lambda_{\mathrm{max}} = \frac{4 \pi^{1/2} m_h}{(m_h^2 - 4 m_\phi^2)^{1/4} } \left( \frac{\Gamma_{\mathrm{SM}} \mathrm{BR}}{1 - \mathrm{BR}} \right)^{1/2}$"
]

# Position each equation on the figure
for i, eq in enumerate(equations):
    ax.text(0.1, 1 - 0.05 * (i + 1), eq, fontsize=12, ha='left', va='top')

# Save to PDF
plt.savefig("DecayWidthDerivation.pdf", format="pdf")
plt.show()



        