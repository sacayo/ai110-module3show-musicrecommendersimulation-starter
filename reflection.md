# Reflection: Profile Comparisons

## High-Energy Pop vs. Chill Lofi

The High-Energy Pop profile (energy 0.8, non-acoustic) and Chill Lofi profile (energy 0.35, acoustic) produced completely non-overlapping top 5 lists — not a single song appeared in both. This makes sense because they sit at opposite ends of two dimensions: energy and acousticness. The pop profile surfaced bright, loud tracks (Sunrise City, Gym Hero), while the lofi profile surfaced quiet, textured ones (Library Rain, Midnight Coding). The scoring correctly separated these two listener archetypes.

## Chill Lofi vs. Conflicting: High Energy + Chill

Both profiles ask for lofi/chill, but the conflicting profile sets energy to 0.95 instead of 0.35. The same three lofi songs appeared in both top 3, but their scores dropped significantly — Midnight Coding went from 4.36 to 3.44 and Library Rain went from 4.50 to 3.30. The ranking order also flipped: Library Rain was #1 for the chill profile (perfect energy match at 0.35) but fell to #2 for the conflicting profile because its energy distance from 0.95 is larger than Midnight Coding's. This shows the system handles contradictory preferences by scoring each dimension independently rather than detecting the conflict — it doesn't warn the user that "high energy lofi" is a contradiction, it just lets the energy penalty accumulate silently.

## High-Energy Pop vs. Intense Rock

Both profiles want high energy and non-acoustic music, but differ on genre and mood. Gym Hero (pop/intense) appeared in both top 5 lists — it ranked #2 for pop (genre match) and #2 for rock (mood match). This dual appearance makes musical sense: a workout pop banger fits both vibes. The key difference is what ranked #1: Sunrise City for pop fans (happy vibe) vs. Storm Runner for rock fans (aggressive vibe). Energy alone can't distinguish these — mood is what separates a sunny pop playlist from a metal workout playlist.

## Intense Rock vs. Acoustic + High Energy

Both profiles target energy 0.9+, but one wants non-acoustic and the other wants acoustic. The Intense Rock top 5 was dominated by loud, electronic/distorted tracks (Storm Runner, Drop Zone, Iron Collapse), while the Acoustic + High Energy profile produced a bizarre mix: Creek Walk (folk, energy 0.31) at #1 followed by four non-acoustic bangers (Drop Zone, Gym Hero, Iron Collapse, Storm Runner) at #2-5. This reveals the acoustic-energy correlation bias in the dataset — there are no high-energy acoustic songs, so the system is forced to choose between satisfying acoustic preference (Creek Walk) or energy preference (everything else). The genre+mood bonus kept Creek Walk on top, but just barely.

## Nonexistent Genre & Mood vs. Everyone Else

The "k-pop/euphoric" profile scored a maximum of 2.22 while every other profile had at least one song above 3.2. With zero genre or mood matches possible, all 20 songs competed purely on energy closeness and acoustic fit — two continuous dimensions that produce a very flat ranking. The top 5 songs (r&b, hip-hop, synthwave, indie pop, soul) have nothing in common musically except mid-range energy near 0.5. This profile exposes the system's biggest limitation: without categorical matches, the recommendations become meaningless. A real system should detect this scenario and either suggest the user try different genre keywords or fall back to a popularity-based ranking.

## Weight Shift Experiment: Energy x2 vs. Original Weights

The most interesting comparison was High-Energy Pop before and after doubling energy weight. With original weights (genre x2, energy x1), Gym Hero ranked #2 and Rooftop Lights ranked #3. After the shift (genre x1, energy x2), they swapped — Rooftop Lights jumped to #2 because its energy (0.76) is closer to the target (0.80) than Gym Hero's (0.93), and losing the genre bonus from 2.0 to 1.0 meant it no longer outweighed the energy advantage. This single weight change made the system feel more musically intuitive: a happy indie pop track really is a better match for a happy pop listener than an intense workout track, even if the workout track technically matches the "pop" genre label.
