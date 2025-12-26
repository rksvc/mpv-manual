document$.subscribe(() => {
	for (const sel of ['.note', '.warning'])
		for (const elem of document.querySelectorAll(sel)) elem.classList.add('admonition')

	/**
	 * @param {Element} node
	 * @param {RegExp} regExp
	 */
	function highlight(node, regExp) {
		if (node.nodeType === Node.TEXT_NODE) {
			const span = document.createElement('span')
			span.innerHTML = node.textContent.replaceAll(
				regExp,
				s => `<mark data-md-highlight>${s}</mark>`,
			)
			node.parentNode.insertBefore(span, node)
			node.parentNode.removeChild(node)
			span.outerHTML = span.innerHTML
		} else for (const child of [...node.childNodes]) highlight(child, regExp)
	}

	for (const dl of document.querySelectorAll('dl')) {
		if (dl.querySelectorAll('& > dt').length < 7) continue

		const input = document.createElement('input')
		dl.parentNode.insertBefore(input, dl)
		input.placeholder = 'Search...'
		input.classList.add('filter')

		let timerId
		input.oninput = () => {
			clearTimeout(timerId)
			timerId = setTimeout(() => {
				timerId = undefined

				const keywords = [...input.value.matchAll(/\w+/g).map(m => m[0])]
				const regExp = new RegExp(keywords.join('|'), 'gi')
				for (const dt of dl.querySelectorAll('& > dt'))
					if (keywords.every(keyword => dt.innerText.includes(keyword))) {
						dt.style.display = dt.nextElementSibling.style.display = ''
						for (const highlight of dt.querySelectorAll('mark'))
							highlight.outerHTML = highlight.innerHTML
						if (keywords.length) highlight(dt, regExp)
					} else {
						dt.style.display = dt.nextElementSibling.style.display = 'none'
					}
			}, 200)
		}
	}
})
