class CupcakeHome {
	constructor() {
		this.cupcakeList = document.querySelector('#cupcake_list');
		this.showCupcakesBtn = document.querySelector('#show_cupcakes');
		this.newCupcakeForm = document.querySelector('#new_cupcake_form');
        this.searchCupcakesInput = document.querySelector('#search_cupcakes')

		this.newCupcakeForm.addEventListener('submit', this.submitNewCupcake.bind(this));
		this.showCupcakesBtn.addEventListener('click', this.showCupcakes.bind(this));
		this.searchCupcakesInput.addEventListener('keyup', this.showCupcakes.bind(this));
	}

	async showCupcakes(evt) {
        let url;
        if (this.searchCupcakesInput.value) {
            url = `/cupcakes/search?cupcake=${this.searchCupcakesInput.value}`
        } else {
            url = '/api/cupcakes'
        }
		const cupcakes = await axios.get(url);
		this.cupcakeList.innerText = '';

		for (let c of cupcakes.data.cupcakes) {
			const newLi = document.createElement('li');
			const newImg = document.createElement('img');
			newImg.classList.add('img-fluid', 'img');
			newImg.setAttribute('src', c.image);
			newImg.style.maxHeight = '150px';
			newLi.innerText = `${c.flavor}, ${c.size} `;
			newLi.classList.add('my-4');
			newLi.append(newImg);
			this.cupcakeList.append(newLi);
		}
	}

	async submitNewCupcake(evt) {

		let flavor = document.getElementById('flavor').value;
		let size = document.getElementById('size').value;
		let image = document.getElementById('image').value || 'https://tinyurl.com/demo-cupcake';
		let rating = document.getElementById('rating').value;

		let formData = {
			flavor,
			size,
			image,
			rating,
		};

		try {
			let response = await axios.post('/api/cupcakes', formData);
			this.newCupcakeForm.reset();
		} catch (error) {
			console.error('Error', error);
		}
	}
}

let thing = new CupcakeHome()