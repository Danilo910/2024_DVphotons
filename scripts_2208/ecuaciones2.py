import matplotlib.pyplot as plt

# Crear una figura para mostrar las ecuaciones
fig, ax = plt.subplots(figsize=(8, 12))
ax.axis('off')  # Ocultar ejes

# Lista de ecuaciones en formato LaTeX
equations = [
    r"$\Gamma(h \to \phi \phi) = \frac{1}{2!} \frac{|\mathcal{M}|^2 P_0}{8 \pi m_h^2}$",
    r"$P_0 = \frac{1}{2} \sqrt{m_h^2 - 4 m_\phi^2} = \frac{m_h}{2} \sqrt{1 - \frac{4 m_\phi^2}{m_h^2}}$",
    r"$\Rightarrow \Gamma(h \to \phi \phi) = \frac{1}{2!} \frac{|\mathcal{M}|^2}{8 \pi m_h^2 2} \left(m_h^2 - 4 m_\phi^2\right)^{1/2}$",
    r"$\mathcal{L} \to \lambda_{hs} \Phi^2 |H|^2 \Rightarrow \lambda_{hs} \Phi^2 \frac{1}{2} (v + h)^2$",
    r"$\Rightarrow |\mathcal{M}|^2 = (\lambda_{hs} v)^2$",
    r"$\Rightarrow \Gamma(h \to \phi \phi) = \frac{1}{4} \frac{\lambda_{hs}^2 V^2}{8 \pi m_h} \sqrt{1 - \frac{4 m_\phi^2}{m_h^2}}$",
    r"$\mathrm{Definimos: } f(m_h, m_\phi, v) = \frac{1}{4} \frac{V^2}{8 \pi m_h} \sqrt{1 - \frac{4 m_\phi^2}{m_h^2}}$",
    r"$\mathrm{Entonces, } \mathrm{BR}(h \to \phi \phi) = \frac{f \lambda_{h\phi}^2}{f \lambda_{h\phi}^2 + \Gamma_\mathrm{SM}} \Rightarrow \lambda^2 = \frac{\Gamma_\mathrm{SM} \mathrm{BR}}{f(1 - \mathrm{BR})}$",
    r"$\Rightarrow \lambda^2 = \frac{\Gamma_\mathrm{SM} \mathrm{BR} (4)(8 \pi m_h)}{(1 - \mathrm{BR}) V^2} \times \frac{1}{\left(1 - \frac{4 m_\phi^2}{m_h^2}\right)^{1/2}}$",
    r"$\Rightarrow \lambda = \left( \frac{\Gamma_\mathrm{SM} \mathrm{BR} (4) 8 \pi m_h}{(1 - \mathrm{BR}) V^2} \right)^{1/2} \frac{1}{\left(1 - \frac{4 m_\phi^2}{m_h^2}\right)^{1/4}}$",
    r"$\Rightarrow \lambda = 2 \left( \frac{\Gamma_\mathrm{SM} \mathrm{BR} 8 \pi m_h}{(1 - \mathrm{BR}) V^2} \right)^{1/2} \frac{1}{\left(1 - \frac{4 m_\phi^2}{m_h^2}\right)^{1/4}}$"
]

# Posicionar cada ecuación en la figura
for i, eq in enumerate(equations):
    ax.text(0.05, 1 - 0.07 * (i + 1), eq, fontsize=12, ha='left', va='top')

# Guardar como PDF
plt.savefig("DecayWidthDerivation_Foto.pdf", format="pdf")
plt.show()



        