class Pagination {

    constructor({
        container,
        page = 1,
        limit = 50,
        total = 0,
        onChange
    }) {

        this.container = document.querySelector(container);
        this.page     = page;
        this.limit    = limit;
        this.total    = total;
        this.onChange = onChange;
    }


    render(){
        if(!this.container)
            return;

        const totalPages = Math.ceil(this.total / this.limit) || 1;

        this.container.innerHTML = `
            <button id="prev" ${this.page <= 1 ? "disabled" : ""} > ◄ </button>


            <span> ${this.page} de ${totalPages} </span>

            <button id="next" ${this.page >= totalPages ? "disabled" : ""} > ► </button>
        `;

        this.container
            .querySelector("#prev")
            .onclick = () => {
                if(this.page > 1){
                    this.page--;
                    this.onChange(this.page);
                }
            };

        this.container
            .querySelector("#next")
            .onclick = () => {
                if(this.page < totalPages){
                    this.page++;
                    this.onChange(this.page);
                }
            };
    }

    update(total,page){
        this.total = total;
        this.page  = page;
        this.render();
    }
}