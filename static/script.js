$(document).ready(function(){
    $('#refresh-button').click(function(){
        $('#loading-spinner').show();
        $('#refresh-button').prop('disabled', true);

        $.ajax({
            url: '/refresh',
            type: 'GET',
            dataType: 'json',
            success: function(data){
                if(data.news_articles){
                    let articlesHtml = '';
                    data.news_articles.forEach(function(article){
                        articlesHtml += `
                            <article class="news-card">
                                ${article.image_url ? `<img src="${article.image_url}" alt="Image for ${article.title}" class="article-image">` : ''}
                                <div class="article-content">
                                    <div class="source-badge">
                                        ${article.source}
                                    </div>
                                    <h2 class="article-title">
                                        <a href="${article.url}" target="_blank">${article.title}</a>
                                    </h2>
                                    <div class="article-meta">
                                        <span><i class="fas fa-clock"></i> ${article.published_at}</span>
                                        ${article.author != "Unknown" ? `<span><i class="fas fa-user"></i> ${article.author}</span>` : ''}
                                    </div>
                                    <p class="article-summary">${article.summary}</p>
                                    <a href="${article.url}" target="_blank" class="read-more">
                                        Read Full Article <i class="fas fa-external-link-alt"></i>
                                    </a>
                                </div>
                            </article>
                        `;
                    });
                    $('#news-articles').html(articlesHtml);
                    $('html, body').animate({ scrollTop: $('#news-articles').offset().top }, 'slow'); // Smooth scroll
                }
            },
            error: function(xhr, status, error){
                $('.error-message').remove(); // Remove existing error messages
                $('.container').prepend(`
                    <div class="error-message">
                        <i class="fas fa-exclamation-circle"></i> Error refreshing news: ${error}
                    </div>
                `);
            },
            complete: function(){
                $('#loading-spinner').hide();
                $('#refresh-button').prop('disabled', false);
            }
        });
    });

    /* Removed filter-btn click event listener */

});