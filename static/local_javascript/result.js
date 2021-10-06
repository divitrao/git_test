const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];
console.log(data)
let kt_table  = document.getElementById('kt_datatable')
let main_div = document.getElementById('result_table')
let elem_table = document.createElement('table')
elem_table.className = 'table '
elem_table.innerHTML = `<thead class="thead-dark">
                            <tr>
                                <th scope='col' > Question </th>
                                <th scope='col' > Answer </th>
                                <th scope='col'> Score </th>
                            </tr>
                        </thead> `
let elem_table_body = document.createElement('tbody')

for(let i=0; i<data['current_result'].length; i++){

    let question = data['current_result'][i]['question']
    let answer = data['current_result'][i]['user_answer']
    let marks = data['current_result'][i]['marks']
    let color
    if(marks==0){
        color = 'success'
    }
    else if(marks==1){
        color = 'primary'
    }
    else if(marks==2){
        color = 'warning'
    }
    else{
        color = 'danger'
    }

    let table_row = document.createElement('tr')
            // table_row.className = `table-success`

    table_row.innerHTML = ` <th class="p-3"> ${question} </th>
                            <td class="p-3"> ${answer}</td>
                            <td class="p-3"><span class="label label-inline label-light-${color} font-weight-bold" style="font-size: 15px;">${marks}</span>  </td>`
                            
                
                            

    

    elem_table_body.appendChild(table_row)
    kt_table.appendChild(elem_table_body)

    
}


if(data['other_result']!=undefined){
    if(data['other_result'].length>=1){
        let other_result_tag = document.getElementById('other_results')
        let div_tag = document.createElement('div')
        div_tag.className = 'row mt-5'
        for(let i=0; i<data['other_result'].length; i++){
            //calculating date and time
            let year = data['other_result'][i][1]['year'] 
            let month = data['other_result'][i][1]['month'] 
            let day = data['other_result'][i][1]['day'] 
            let hour = data['other_result'][i][1]['hour'] 
            let minute = data['other_result'][i][1]['minute'] 
            
            let card_holder = document.createElement('div')
            card_holder.innerHTML = `<div class="card card-custom m-5">
                                       
                                        <div class="card-body text-center">
                                        Result for test given on ${monthNames[month-1]}/${day}/${year} 
                                        </div>
                                        <div class="card-footer d-flex justify-content-between">
                                            <button class="btn btn-outline-primary"> Score: ${data['other_result'][i][2]['marks_achieved']}</button>
                                            <a href="/quiz/result/${data['other_result'][i][0]}/" class="btn btn-outline-success  font-weight-bold">View</a>
                                        </div>
                                    </div>`
            
            other_result_tag.appendChild(card_holder)
            


        }
        
    }
}

