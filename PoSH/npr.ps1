cls

function parse-article($text,$url_){

    $body = $text[4..($text.Count)] -join "`r`n"

    [pscustomobject]@{
        link=$url_
        Title=$text[2]
        By=$text[3]
        Body=$body
        LenBody=$body.length
    }
}

function get-article() {
    param($url)
    $url
    $text=
          (iwr $url).allelements |
          where { $_.tagName -eq 'p' } |
            foreach {
               $_.innertext
            }

    parse-article $text $url
}

function put-LUU(){
    param($s, $p, $o)

    $url = 'http://www.agentidea.com:80/api/allegro/tripleLUU'
    $o_ = $o.substring(7)
    $o_
    $params = @{
        repo='news'
        ns='rdf.agentidea.com'
        sub=$s
        pred = $p
        obj = $o_
        }

Invoke-RestMethod -Uri $url -Method Post -Body $params

}


function put-UUU(){
    param($s, $p, $o)

    $url = 'http://www.agentidea.com:80/api/allegro/triple'

    $params = @{
        repo='news'
        ns='rdf.agentidea.com'
        sub=$s
        pred = $p
        obj = $o
        }

Invoke-RestMethod -Uri $url -Method Post -Body $params

}

function put-LUL(){
    param($s, $p, $o, $type='string')

    $url = 'http://www.agentidea.com:80/api/allegro/tripleUUL'

    $params = @{
        repo='news'
        ns='rdf.agentidea.com'
        sub=$s
        pred = $p
        obj = $o
        type = $type
    }

    Invoke-RestMethod -Uri $url -Method Post -Body $params
}


function put-UUL(){
    param($s, $p, $o, $type='string')

    $url = 'http://www.agentidea.com:80/api/allegro/tripleUUL'

    $params = @{
        repo='news'
        ns='rdf.agentidea.com'
        sub=$s
        pred = $p
        obj = $o
        type = $type
    }

    Invoke-RestMethod -Uri $url -Method Post -Body $params
}

function Get-StringHash([String] $String,$HashName = "MD5")
{
    $StringBuilder = New-Object System.Text.StringBuilder
    [System.Security.Cryptography.HashAlgorithm]::Create($HashName).ComputeHash([System.Text.Encoding]::UTF8.GetBytes($String))|%{
        [Void]$StringBuilder.Append($_.ToString("x2"))
    }
    $StringBuilder.ToString()
}

function publish-article(){
    [CmdletBinding()]
    param($articles)

   $articles | foreach{
        if($_.By -ne $null -and $_.By.trim() -ne ""){

            $urlHash_ = Get-StringHash $_.link
            $date = Get-Date

            put-LUL  $urlHash_ "spec/news/#term_date" $date.ToUniversalTime()
            put-LUL  $urlHash_ "spec/news/#term_Day"$date.Day
            put-LUL  $urlHash_ "spec/news/#term_DayOfWeek"$date.DayOfWeek
            put-LUL  $urlHash_ "spec/news/#term_DayOfYear"$date.DayOfYear
            put-LUL  $urlHash_ "spec/news/#term_Year"$date.Year
            put-LUL  $urlHash_ "spec/news/#term_Month"$date.Month
            put-LUL  $urlHash_ "spec/news/#term_Hour"$date.Hour
            put-LUL  $urlHash_ "spec/news/#term_src" $_.link
            put-LUL  $urlHash_ "spec/news/#term_author" $_.By
            put-LUL  $urlHash_ "spec/news/#term_title" $_.Title
            put-LUL  $urlHash_ "spec/news/#term_body" $_.Body
            put-LUL  $urlHash_ "spec/news/#term_category" "arts & life"
        }
    }

}

function get-articles(){
    [CmdletBinding()]         #adds debug options + a ton of other things ...
    param($links)

    $finalparse = $links |
        foreach {
            get-article $_
        }

    $finalparse
}

function start-processing(){
    $base_url = "http://thin.npr.org"
    #$news_page = iwr "$base_url/t.php?tid=1001"
    $news_page = iwr "$base_url/t.php?tid=1008"
    $top_links = $news_page.allelements | where { $_.tagName -eq 'a' -and $_.href -match 'php'} | select href*,innerText
    $top_links | %{ $base_url + $_.href + '&x=1' }

}

Start-Transcript
$full_links = start-processing
$articlesAll = get-articles $full_links -Verbose
publish-article $articlesAll -Verbose
Stop-Transcript
