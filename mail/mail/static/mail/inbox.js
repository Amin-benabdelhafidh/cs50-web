document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => {load_mailbox('archive')});
  document.querySelector('#compose').addEventListener('click', () => { 
    compose_email()
    document.querySelector('#compose-form').addEventListener('submit', () => {
      const rec = document.querySelector('#compose-recipients').value;
      const sub = document.querySelector('#compose-subject').value;
      const bod = document.querySelector('#compose-body').value;
      sendEmail(rec, sub, bod);
    }); 
  });
  

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3 class="h-styles" id='mailbox-name'>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);
    for(let i = 0; i<email.length;i++){
      // create element
      const element = document.createElement('div');

      // create the childs of the element
      const sender_recipients = document.createElement('h4');
      if(mailbox === 'inbox'){sender_recipients.innerHTML = email[i].sender;}
      else{sender_recipients.innerHTML = email[i].recipients;}
      const subject = document.createElement('h6');
      subject.innerHTML = email[i].subject;
      const date = document.createElement('p');
      date.innerHTML = email[i].timestamp;

      // set class attributes to our elements
      sender_recipients.setAttribute("class", 'h-styles');
      subject.setAttribute("class", 'subject');
      date.setAttribute("class", 'timestamp');

      // append childs to the div-elements
      element.append(sender_recipients);
      element.append(subject);
      element.append(date);

      // set class attribute to the div-element
      element.setAttribute("class", 'div-1');

      // listen to the element's click-event
      subject.addEventListener('click', () => {
        console.log('This element has been clicked!');
        viewEmail(email[i].id, mailbox);
      });

      document.querySelector('#emails-view').append(element);
    }
  });
}

function sendEmail(rec, sub, bod){
  // sending the email to the server
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: rec,
        subject: sub,
        body: bod
    })
  })
  .then(response => response.json())
  .then(result => {
      
      console.log(result);
  })
  .catch(error => {
      console.log(error)
  });
}

function viewEmail(id, mailbox){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);

    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#view-email').style.display = 'block';

    document.querySelector('#sender').innerHTML = email.sender
    document.querySelector('#recipients').innerHTML = email.recipients
    document.querySelector('#subject').innerHTML = email.subject
    document.querySelector('#timestamp').innerHTML = email.timestamp
    document.querySelector('#body').innerHTML = email.body

    const un_archive = document.querySelector('#archive-button');
    if(mailbox === 'archive'){
      un_archive.style.display = 'inline';
      un_archive.innerHTML = 'Unarchive';
    } else if(mailbox === 'inbox'){
      un_archive.style.display = 'inline';
      un_archive.innerHTML = 'Archive';
    } else if(mailbox === 'sent'){
      un_archive.style.display = 'none';
    }
    un_archive.addEventListener('click', () => {
      archive(email.id, mailbox);
    })

    document.querySelector('#reply-button').addEventListener('click', () => {
      // Show compose view and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#view-email').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';
      document.querySelector('#view-email').innerHTML = 'Reply';
      reply(email.sender, email.subject, email.timestamp, email.body);
      document.querySelector('#compose-form').addEventListener('submit', () => {
        const rec = document.querySelector('#compose-recipients').value;
        const sub = document.querySelector('#compose-subject').value;
        const bod = document.querySelector('#compose-body').value;
        sendEmail(rec, sub, bod);
      });
    })

  })
  .catch(error => console.log(error));
  // mark email as read
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  .catch(error => console.log(error));
}


function archive(id ,mailbox){
  // archive
  if(mailbox === 'inbox'){
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
  }
  // unarchive 
  else {
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
  }
}

function reply(sender, subject, timestamp, body){

  document.querySelector('#compose-recipients').value = `${sender}`
  if(subject[0] === 'R' && subject[1] === 'e' && subject[2] === ':'){
    document.querySelector('#compose-subject').value= `${subject}`
  } else {
    document.querySelector('#compose-subject').value = `Re: ${subject}`
  }
  document.querySelector('#compose-body').innerHTML = `On ${timestamp} ${sender} wrote: ${body}`

}
