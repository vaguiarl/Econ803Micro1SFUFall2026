from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
start_marker = r"""\begin_layout Standard
We use the Envelope's theorem 
\end_layout"""
end_marker = r"""\begin_layout Standard
This provides the Roy's identity"""
start = s.index(start_marker)
end = s.index(end_marker, start)
replacement = r'''\begin_layout Standard
Assume the maximizer is unique and the value function is differentiable.  The envelope theorem applied to
\end_layout

\begin_layout Standard
\begin_inset Formula 
\[
v(p,w)=\max_{x\geq0,\;p\cdot x\leq w}u(x)
\]
\end_inset
\end_layout

\begin_layout Standard
gives
\end_layout

\begin_layout Standard
\begin_inset Formula 
\[
\partial_w v(p,w)=\lambda(p,w),\qquad \nabla_p v(p,w)=-\lambda(p,w)x(p,w).
\]
\end_inset
\end_layout

'''
path.write_text(s[:start] + replacement + s[end:])
print("repaired Roy setup")
