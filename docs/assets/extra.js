document$.subscribe(() => {
	for (const sel of ['.note', '.warning'])
		for (const elem of document.querySelectorAll(sel)) elem.classList.add('admonition')
})
